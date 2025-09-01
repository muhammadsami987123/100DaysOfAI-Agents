import openai
import json
import re
import logging
from typing import Dict, List, Any, Optional
import base64
import os
from datetime import datetime
import uuid
import io
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from config import Config, DEFAULT_THEMES, DIAGRAM_TYPES, EXPORT_FORMATS

logger = logging.getLogger(__name__)

class MindMapAgent:
    """AI-powered mind map diagram generator"""
    
    def __init__(self):
        self.config = Config()
        self.openai_client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for file storage"""
        directories = [
            self.config.UPLOAD_DIR,
            self.config.EXPORT_DIR,
            self.config.TEMP_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def generate_mindmap(
        self,
        text_input: str,
        diagram_type: str = "mindmap",
        theme: str = "light",
        depth_levels: int = 3,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate a mind map from unstructured text input
        """
        try:
            # Validate input
            if len(text_input) > self.config.MAX_INPUT_LENGTH:
                raise ValueError(f"Input text too long. Maximum {self.config.MAX_INPUT_LENGTH} characters allowed.")
            
            if depth_levels > self.config.MAX_DEPTH_LEVELS:
                depth_levels = self.config.MAX_DEPTH_LEVELS
            
            # Process text with AI
            structured_data = await self._process_text_with_ai(
                text_input, diagram_type, depth_levels, language
            )
            
            # Generate diagram code
            diagram_code = self._generate_diagram_code(
                structured_data, diagram_type, theme
            )
            
            # Create response
            result = {
                "success": True,
                "diagram_type": diagram_type,
                "theme": theme,
                "depth_levels": depth_levels,
                "language": language,
                "structured_data": structured_data,
                "diagram_code": diagram_code,
                "mermaid_code": self._generate_mermaid_code(structured_data, diagram_type, theme),
                "timestamp": datetime.now().isoformat(),
                "session_id": str(uuid.uuid4())
            }
            
            logger.info(f"Successfully generated mindmap with {len(structured_data.get('nodes', []))} nodes")
            return result
            
        except Exception as e:
            logger.error(f"Error generating mindmap: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _process_text_with_ai(
        self,
        text_input: str,
        diagram_type: str,
        depth_levels: int,
        language: str
    ) -> Dict[str, Any]:
        """
        Process text input with OpenAI to extract structured data
        """
        # Create the prompt based on diagram type
        prompt = self._create_ai_prompt(text_input, diagram_type, depth_levels, language)
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing text and creating structured hierarchical diagrams. You must respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.OPENAI_MAX_TOKENS,
                temperature=self.config.OPENAI_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            structured_data = json.loads(content)
            
            # Validate and clean the structured data
            structured_data = self._validate_structured_data(structured_data, diagram_type)
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing text with AI: {str(e)}")
            # Fallback to simple text processing
            return self._fallback_text_processing(text_input, diagram_type, depth_levels)
    
    def _create_ai_prompt(
        self,
        text_input: str,
        diagram_type: str,
        depth_levels: int,
        language: str
    ) -> str:
        """
        Create AI prompt for text processing
        """
        diagram_info = DIAGRAM_TYPES.get(diagram_type, DIAGRAM_TYPES["mindmap"])
        
        if diagram_type == "mindmap":
            prompt = f"""
Analyze the following text and create a hierarchical mind map structure with up to {depth_levels} levels of depth.

Text to analyze:
{text_input}

Requirements:
- Create a hierarchical structure with a central topic and related subtopics
- Limit to {depth_levels} levels maximum
- Each node should have a clear, concise label
- Maintain logical relationships between concepts
- Use the language: {language}

For mind maps:
- Focus on central topic with radiating branches
- Group related concepts together
- Use clear, descriptive labels

Respond with a JSON object in this exact format:
{{
    "title": "Main topic title",
    "description": "Brief description of the diagram",
    "nodes": [
        {{
            "id": "unique_id_1",
            "label": "Node label",
            "level": 1,
            "parent": null,
            "children": ["child_id_1", "child_id_2"]
        }},
        {{
            "id": "child_id_1",
            "label": "Child node label",
            "level": 2,
            "parent": "unique_id_1",
            "children": []
        }}
    ],
    "relationships": [
        {{
            "from": "node_id_1",
            "to": "node_id_2",
            "label": "relationship description (optional)"
        }}
    ]
}}

Ensure the JSON is valid and follows the exact structure above.
"""
        elif diagram_type == "flowchart":
            prompt = f"""
Analyze the following text and create a flowchart structure showing processes and decisions with up to {depth_levels} levels.

Text to analyze:
{text_input}

Requirements:
- Create a process flow diagram showing steps and decision points
- Limit to {depth_levels} levels maximum
- Each node should represent a step, process, or decision
- Use clear, action-oriented labels
- Use the language: {language}

For flowcharts:
- Start with an input/beginning node
- Show process steps as rectangles
- Show decision points as diamonds
- End with an output/ending node
- Use arrows to show flow direction

Respond with a JSON object in this exact format:
{{
    "title": "Process Flow Title",
    "description": "Brief description of the process",
    "nodes": [
        {{
            "id": "start",
            "label": "Start",
            "level": 1,
            "type": "start",
            "parent": null,
            "children": ["step1"]
        }},
        {{
            "id": "step1",
            "label": "Process Step",
            "level": 2,
            "type": "process",
            "parent": "start",
            "children": ["decision1"]
        }},
        {{
            "id": "decision1",
            "label": "Decision Point?",
            "level": 3,
            "type": "decision",
            "parent": "step1",
            "children": ["yes_path", "no_path"]
        }}
    ],
    "relationships": [
        {{
            "from": "start",
            "to": "step1",
            "label": ""
        }},
        {{
            "from": "decision1",
            "to": "yes_path",
            "label": "Yes"
        }},
        {{
            "from": "decision1",
            "to": "no_path",
            "label": "No"
        }}
    ]
}}

Ensure the JSON is valid and follows the exact structure above.
"""
        elif diagram_type == "orgchart":
            prompt = f"""
Analyze the following text and create an organizational chart structure showing hierarchical relationships with up to {depth_levels} levels.

Text to analyze:
{text_input}

Requirements:
- Create an organizational hierarchy showing reporting relationships
- Limit to {depth_levels} levels maximum
- Each node should represent a role, position, or department
- Use clear, professional labels
- Use the language: {language}

For organizational charts:
- Start with the top-level position (CEO, Director, etc.)
- Show reporting relationships clearly
- Use appropriate titles and roles
- Group related departments or teams

Respond with a JSON object in this exact format:
{{
    "title": "Organization Structure",
    "description": "Brief description of the organization",
    "nodes": [
        {{
            "id": "ceo",
            "label": "CEO / Director",
            "level": 1,
            "type": "executive",
            "parent": null,
            "children": ["manager1", "manager2"]
        }},
        {{
            "id": "manager1",
            "label": "Department Manager",
            "level": 2,
            "type": "manager",
            "parent": "ceo",
            "children": ["employee1", "employee2"]
        }}
    ],
    "relationships": [
        {{
            "from": "ceo",
            "to": "manager1",
            "label": "reports to"
        }}
    ]
}}

Ensure the JSON is valid and follows the exact structure above.
"""
        else:  # network
            prompt = f"""
Analyze the following text and create a network diagram structure showing connections and relationships with up to {depth_levels} levels.

Text to analyze:
{text_input}

Requirements:
- Create a network diagram showing interconnected nodes
- Limit to {depth_levels} levels maximum
- Each node should represent a concept, entity, or component
- Show relationships and connections between nodes
- Use the language: {language}

For network diagrams:
- Focus on connections and relationships
- Show how different elements interact
- Use clear, descriptive labels
- Highlight key connections

Respond with a JSON object in this exact format:
{{
    "title": "Network Diagram",
    "description": "Brief description of the network",
    "nodes": [
        {{
            "id": "node1",
            "label": "Central Node",
            "level": 1,
            "type": "central",
            "parent": null,
            "children": ["node2", "node3"]
        }},
        {{
            "id": "node2",
            "label": "Connected Node",
            "level": 2,
            "type": "connected",
            "parent": "node1",
            "children": []
        }}
    ],
    "relationships": [
        {{
            "from": "node1",
            "to": "node2",
            "label": "connects to"
        }}
    ]
}}

Ensure the JSON is valid and follows the exact structure above.
"""
        
        return prompt
    
    def _validate_structured_data(
        self,
        data: Dict[str, Any],
        diagram_type: str
    ) -> Dict[str, Any]:
        """
        Validate and clean structured data from AI
        """
        # Ensure required fields exist
        if "title" not in data:
            data["title"] = "Untitled Diagram"
        
        if "nodes" not in data:
            data["nodes"] = []
        
        if "relationships" not in data:
            data["relationships"] = []
        
        # Clean and validate nodes
        valid_nodes = []
        node_ids = set()
        
        for node in data["nodes"]:
            if isinstance(node, dict) and "id" in node and "label" in node:
                # Ensure unique IDs
                if node["id"] in node_ids:
                    node["id"] = f"{node['id']}_{len(node_ids)}"
                
                node_ids.add(node["id"])
                
                # Ensure required fields
                node.setdefault("level", 1)
                node.setdefault("parent", None)
                node.setdefault("children", [])
                node.setdefault("type", "default")
                
                # Clean label
                node["label"] = str(node["label"]).strip()
                if len(node["label"]) > 50:
                    node["label"] = node["label"][:47] + "..."
                
                valid_nodes.append(node)
        
        data["nodes"] = valid_nodes
        
        # Limit number of nodes
        if len(data["nodes"]) > self.config.MAX_NODES:
            data["nodes"] = data["nodes"][:self.config.MAX_NODES]
        
        return data
    
    def _fallback_text_processing(
        self,
        text_input: str,
        diagram_type: str,
        depth_levels: int
    ) -> Dict[str, Any]:
        """
        Fallback text processing when AI fails
        """
        # Simple text processing
        lines = text_input.split('\n')
        words = text_input.split()
        
        # Create a simple structure
        nodes = []
        node_id = 1
        
        # Main topic
        main_topic = words[0] if words else "Main Topic"
        nodes.append({
            "id": f"node_{node_id}",
            "label": main_topic,
            "level": 1,
            "parent": None,
            "children": [],
            "type": "central"
        })
        node_id += 1
        
        # Add some key concepts
        key_concepts = list(set([word for word in words if len(word) > 3]))[:10]
        
        for concept in key_concepts:
            nodes.append({
                "id": f"node_{node_id}",
                "label": concept,
                "level": 2,
                "parent": "node_1",
                "children": [],
                "type": "subtopic"
            })
            node_id += 1
        
        return {
            "title": main_topic,
            "description": f"Generated {diagram_type} from text input",
            "nodes": nodes,
            "relationships": []
        }
    
    def _generate_diagram_code(
        self,
        structured_data: Dict[str, Any],
        diagram_type: str,
        theme: str
    ) -> str:
        """
        Generate diagram code for rendering
        """
        if diagram_type == "mindmap":
            return self._generate_mindmap_code(structured_data, theme)
        elif diagram_type == "flowchart":
            return self._generate_flowchart_code(structured_data, theme)
        elif diagram_type == "orgchart":
            return self._generate_orgchart_code(structured_data, theme)
        else:
            return self._generate_network_code(structured_data, theme)
    
    def _generate_mermaid_code(
        self,
        structured_data: Dict[str, Any],
        diagram_type: str,
        theme: str
    ) -> str:
        """
        Generate Mermaid.js code for the diagram
        """
        theme_colors = DEFAULT_THEMES.get(theme, DEFAULT_THEMES["light"])
        
        if diagram_type == "mindmap":
            return self._generate_mermaid_mindmap(structured_data, theme_colors)
        elif diagram_type == "flowchart":
            return self._generate_mermaid_flowchart(structured_data, theme_colors)
        else:
            return self._generate_mermaid_graph(structured_data, theme_colors)
    
    def _generate_mermaid_mindmap(
        self,
        data: Dict[str, Any],
        theme_colors: Dict[str, str]
    ) -> str:
        """
        Generate Mermaid mindmap code
        """
        title = data.get('title', 'Main Topic')
        
        # Build the mindmap structure
        nodes_by_parent = {}
        for node in data.get('nodes', []):
            parent = node.get('parent')
            if parent not in nodes_by_parent:
                nodes_by_parent[parent] = []
            nodes_by_parent[parent].append(node)
        
        # Start with basic mindmap structure
        mermaid_code = "%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '" + theme_colors["primary"] + "', 'primaryTextColor': '" + theme_colors["text"] + "', 'primaryBorderColor': '" + theme_colors["primary"] + "', 'lineColor': '" + theme_colors["secondary"] + "', 'secondaryColor': '" + theme_colors["secondary"] + "', 'tertiaryColor': '" + theme_colors["accent"] + "' }}}%%\n"
        mermaid_code += "mindmap\n"
        mermaid_code += f"  root(({title}))"
        
        # Add child nodes recursively
        def add_children(parent_id, indent=2):
            nonlocal mermaid_code
            children = nodes_by_parent.get(parent_id, [])
            for child in children:
                mermaid_code += f"\n{'  ' * indent}{child['label']}"
                add_children(child['id'], indent + 1)
        
        add_children(None)
        return mermaid_code
    
    def _generate_mermaid_flowchart(
        self,
        data: Dict[str, Any],
        theme_colors: Dict[str, str]
    ) -> str:
        """
        Generate Mermaid flowchart code
        """
        mermaid_code = "%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '" + theme_colors["primary"] + "', 'primaryTextColor': '" + theme_colors["text"] + "', 'primaryBorderColor': '" + theme_colors["primary"] + "', 'lineColor': '" + theme_colors["secondary"] + "', 'secondaryColor': '" + theme_colors["secondary"] + "', 'tertiaryColor': '" + theme_colors["accent"] + "' }}}%%\n"
        mermaid_code += "flowchart TD"
        
        # Add nodes
        for node in data.get('nodes', []):
            node_id = node['id']
            label = node['label']
            node_type = node.get('type', 'default')
            
            if node_type == 'start':
                mermaid_code += f"\n    {node_id}([{label}])"
            elif node_type == 'decision':
                mermaid_code += f"\n    {node_id}{{{label}}}"
            elif node_type == 'end':
                mermaid_code += f"\n    {node_id}([{label}])"
            else:
                mermaid_code += f"\n    {node_id}[{label}]"
        
        # Add relationships
        for rel in data.get('relationships', []):
            from_node = rel.get('from')
            to_node = rel.get('to')
            label = rel.get('label', '')
            if from_node and to_node:
                if label:
                    mermaid_code += f"\n    {from_node} -->|{label}| {to_node}"
                else:
                    mermaid_code += f"\n    {from_node} --> {to_node}"
        
        return mermaid_code
    
    def _generate_mermaid_graph(
        self,
        data: Dict[str, Any],
        theme_colors: Dict[str, str]
    ) -> str:
        """
        Generate Mermaid graph code for org charts and networks
        """
        mermaid_code = "%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '" + theme_colors["primary"] + "', 'primaryTextColor': '" + theme_colors["text"] + "', 'primaryBorderColor': '" + theme_colors["primary"] + "', 'lineColor': '" + theme_colors["secondary"] + "', 'secondaryColor': '" + theme_colors["secondary"] + "', 'tertiaryColor': '" + theme_colors["accent"] + "' }}}%%\n"
        mermaid_code += "graph TD"
        
        # Add nodes
        for node in data.get('nodes', []):
            node_id = node['id']
            label = node['label']
            level = node.get('level', 1)
            node_type = node.get('type', 'default')
            
            # Different node styles based on level and type
            if level == 1 or node_type == 'executive':
                mermaid_code += f"\n    {node_id}([{label}])"
            elif node_type == 'manager':
                mermaid_code += f"\n    {node_id}([{label}])"
            else:
                mermaid_code += f"\n    {node_id}[{label}]"
        
        # Add relationships
        for rel in data.get('relationships', []):
            from_node = rel.get('from')
            to_node = rel.get('to')
            label = rel.get('label', '')
            if from_node and to_node:
                if label:
                    mermaid_code += f"\n    {from_node} -->|{label}| {to_node}"
                else:
                    mermaid_code += f"\n    {from_node} --> {to_node}"
        
        return mermaid_code
    
    def _generate_mindmap_code(
        self,
        data: Dict[str, Any],
        theme: str
    ) -> str:
        """Generate custom mindmap code"""
        return json.dumps(data, indent=2)
    
    def _generate_flowchart_code(
        self,
        data: Dict[str, Any],
        theme: str
    ) -> str:
        """Generate custom flowchart code"""
        return json.dumps(data, indent=2)
    
    def _generate_orgchart_code(
        self,
        data: Dict[str, Any],
        theme: str
    ) -> str:
        """Generate custom org chart code"""
        return json.dumps(data, indent=2)
    
    def _generate_network_code(
        self,
        data: Dict[str, Any],
        theme: str
    ) -> str:
        """Generate custom network code"""
        return json.dumps(data, indent=2)
    
    async def export_diagram(
        self,
        diagram_data: str,
        export_format: str = "png",
        filename: str = "mindmap"
    ) -> Dict[str, Any]:
        """
        Export the diagram in various formats
        """
        try:
            # Parse diagram data
            if isinstance(diagram_data, str):
                data = json.loads(diagram_data)
            else:
                data = diagram_data
            
            # Generate export
            if export_format == "json":
                return await self._export_json(data, filename)
            elif export_format == "svg":
                return await self._export_svg(data, filename)
            elif export_format == "png":
                return await self._export_png(data, filename)
            elif export_format == "pdf":
                return await self._export_pdf(data, filename)
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
                
        except Exception as e:
            logger.error(f"Error exporting diagram: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _export_json(
        self,
        data: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """Export as JSON file"""
        file_path = os.path.join(self.config.EXPORT_DIR, f"{filename}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "format": "json",
            "filename": f"{filename}.json",
            "file_path": file_path,
            "download_url": f"/exports/{filename}.json"
        }
    
    async def _export_svg(
        self,
        data: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """Export as SVG file"""
        try:
            # Create a simple SVG representation
            svg_content = self._generate_svg_content(data)
            file_path = os.path.join(self.config.EXPORT_DIR, f"{filename}.svg")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            return {
                "success": True,
                "format": "svg",
                "filename": f"{filename}.svg",
                "file_path": file_path,
                "download_url": f"/exports/{filename}.svg"
            }
        except Exception as e:
            logger.error(f"Error generating SVG: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to generate SVG: {str(e)}"
            }
    
    async def _export_png(
        self,
        data: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """Export as PNG file"""
        try:
            # Create a matplotlib-based diagraExport Your Diagramm
            img_data = self._generate_png_content(data)
            file_path = os.path.join(self.config.EXPORT_DIR, f"{filename}.png")
            
            with open(file_path, 'wb') as f:
                f.write(img_data)
            
            return {
                "success": True,
                "format": "png",
                "filename": f"{filename}.png",
                "file_path": file_path,
                "download_url": f"/exports/{filename}.png"
            }
        except Exception as e:
            logger.error(f"Error generating PNG: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to generate PNG: {str(e)}"
            }
    
    async def _export_pdf(
        self,
        data: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """Export as PDF file"""
        try:
            # Create a simple PDF representation
            pdf_content = self._generate_pdf_content(data)
            file_path = os.path.join(self.config.EXPORT_DIR, f"{filename}.pdf")
            
            with open(file_path, 'wb') as f:
                f.write(pdf_content)
            
            return {
                "success": True,
                "format": "pdf",
                "filename": f"{filename}.pdf",
                "file_path": file_path,
                "download_url": f"/exports/{filename}.pdf"
            }
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to generate PDF: {str(e)}"
            }
    
    def _generate_svg_content(self, data: Dict[str, Any]) -> str:
        """Generate SVG content for the diagram"""
        title = data.get('title', 'Diagram')
        nodes = data.get('nodes', [])
        
        # Calculate dimensions
        width = 800
        height = 600
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .node {{ fill: #3b82f6; stroke: #1d4ed8; stroke-width: 2; }}
            .node-text {{ fill: white; font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }}
            .connection {{ stroke: #6b7280; stroke-width: 2; fill: none; }}
            .title {{ fill: #1f2937; font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; text-anchor: middle; }}
        </style>
    </defs>
    
    <rect width="{width}" height="{height}" fill="white"/>
    <text x="{width//2}" y="40" class="title">{title}</text>
'''
        
        # Add nodes
        for i, node in enumerate(nodes[:10]):  # Limit to 10 nodes for SVG
            x = 100 + (i % 3) * 200
            y = 100 + (i // 3) * 100
            svg += f'''
    <circle cx="{x}" cy="{y}" r="30" class="node"/>
    <text x="{x}" y="{y+4}" class="node-text">{node['label'][:10]}</text>'''
        
        svg += '''
</svg>'''
        
        return svg
    
    def _generate_png_content(self, data: Dict[str, Any]) -> bytes:
        """Generate PNG content for the diagram"""
        try:
            title = data.get('title', 'Diagram')
            nodes = data.get('nodes', [])
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.axis('off')
            
            # Add title
            ax.text(5, 7.5, title, fontsize=20, fontweight='bold', ha='center', va='center')
            
            # Create network graph
            G = nx.Graph()
            
            # Add nodes
            for node in nodes:
                G.add_node(node['id'], label=node['label'], level=node.get('level', 1))
            
            # Add edges based on parent-child relationships
            for node in nodes:
                if node.get('parent'):
                    G.add_edge(node['parent'], node['id'])
            
            # Position nodes using spring layout
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, ax=ax)
            
            # Add labels
            labels = {node: G.nodes[node]['label'][:15] for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold', ax=ax)
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            plt.close()
            
            return buf.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating PNG: {str(e)}")
            # Return a simple error image
            return self._generate_error_image()
    
    def _generate_pdf_content(self, data: Dict[str, Any]) -> bytes:
        """Generate PDF content for the diagram"""
        try:
            # For now, return a simple PDF with text
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            
            # Add title
            c.setFont("Helvetica-Bold", 24)
            c.drawString(100, 750, data.get('title', 'Diagram'))
            
            # Add nodes
            c.setFont("Helvetica", 12)
            y = 700
            for node in data.get('nodes', [])[:20]:  # Limit to 20 nodes
                c.drawString(100, y, f"• {node['label']}")
                y -= 20
                if y < 50:
                    break
            
            c.save()
            buf.seek(0)
            return buf.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return b''
    
    def _generate_error_image(self) -> bytes:
        """Generate a simple error image"""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Error generating diagram', 
                   ha='center', va='center', fontsize=16, transform=ax.transAxes)
            ax.axis('off')
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            return buf.getvalue()
        except:
            return b''
