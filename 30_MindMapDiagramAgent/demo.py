#!/usr/bin/env python3
"""
Demo script for MindMapDiagramAgent
Shows examples of different diagram types
"""

import asyncio
import json
from mindmap_agent import MindMapAgent

async def demo_mindmap():
    """Demo mind map generation"""
    print("🧠 Generating Mind Map...")
    
    text = """
    Artificial Intelligence
    - Machine Learning
      - Supervised Learning
        - Classification
        - Regression
      - Unsupervised Learning
        - Clustering
        - Dimensionality Reduction
    - Natural Language Processing
      - Text Analysis
      - Language Generation
      - Translation
    - Computer Vision
      - Image Recognition
      - Object Detection
      - Image Segmentation
    """
    
    agent = MindMapAgent()
    result = await agent.generate_mindmap(
        text_input=text,
        diagram_type="mindmap",
        theme="light",
        depth_levels=3
    )
    
    if result["success"]:
        print("✅ Mind Map generated successfully!")
        print(f"   Nodes: {len(result['structured_data']['nodes'])}")
        print(f"   Title: {result['structured_data']['title']}")
    else:
        print(f"❌ Failed: {result['error']}")

async def demo_flowchart():
    """Demo flowchart generation"""
    print("\n📊 Generating Flowchart...")
    
    text = """
    User Registration Process
    1. User visits website
    2. Clicks register button
    3. Fills registration form
    4. Validates email
    5. If email valid: Create account
    6. If email invalid: Show error
    7. Send welcome email
    8. Redirect to dashboard
    """
    
    agent = MindMapAgent()
    result = await agent.generate_mindmap(
        text_input=text,
        diagram_type="flowchart",
        theme="blue",
        depth_levels=4
    )
    
    if result["success"]:
        print("✅ Flowchart generated successfully!")
        print(f"   Nodes: {len(result['structured_data']['nodes'])}")
        print(f"   Title: {result['structured_data']['title']}")
    else:
        print(f"❌ Failed: {result['error']}")

async def demo_orgchart():
    """Demo organizational chart generation"""
    print("\n🏢 Generating Organization Chart...")
    
    text = """
    Company Structure
    - CEO
      - CTO
        - Software Development
        - Infrastructure
        - Quality Assurance
      - CFO
        - Accounting
        - Finance
        - HR
      - CMO
        - Marketing
        - Sales
        - Customer Support
    """
    
    agent = MindMapAgent()
    result = await agent.generate_mindmap(
        text_input=text,
        diagram_type="orgchart",
        theme="purple",
        depth_levels=3
    )
    
    if result["success"]:
        print("✅ Organization Chart generated successfully!")
        print(f"   Nodes: {len(result['structured_data']['nodes'])}")
        print(f"   Title: {result['structured_data']['title']}")
    else:
        print(f"❌ Failed: {result['error']}")

async def demo_network():
    """Demo network diagram generation"""
    print("\n🌐 Generating Network Diagram...")
    
    text = """
    Social Network Connections
    - Alice
      - Friends with Bob
      - Friends with Charlie
      - Works with David
    - Bob
      - Friends with Alice
      - Friends with Eve
      - Family with Frank
    - Charlie
      - Friends with Alice
      - Colleague with Grace
    """
    
    agent = MindMapAgent()
    result = await agent.generate_mindmap(
        text_input=text,
        diagram_type="network",
        theme="green",
        depth_levels=2
    )
    
    if result["success"]:
        print("✅ Network Diagram generated successfully!")
        print(f"   Nodes: {len(result['structured_data']['nodes'])}")
        print(f"   Title: {result['structured_data']['title']}")
    else:
        print(f"❌ Failed: {result['error']}")

async def demo_export():
    """Demo export functionality"""
    print("\n📤 Testing Export Functionality...")
    
    # Sample data
    sample_data = {
        "title": "Sample Diagram",
        "description": "A sample diagram for testing export",
        "nodes": [
            {"id": "node1", "label": "Main Topic", "level": 1, "parent": None, "children": ["node2", "node3"]},
            {"id": "node2", "label": "Subtopic 1", "level": 2, "parent": "node1", "children": []},
            {"id": "node3", "label": "Subtopic 2", "level": 2, "parent": "node1", "children": []}
        ],
        "relationships": []
    }
    
    agent = MindMapAgent()
    
    # Test JSON export
    result = await agent.export_diagram(sample_data, "json", "demo")
    if result["success"]:
        print("✅ JSON export successful!")
    else:
        print(f"❌ JSON export failed: {result['error']}")
    
    # Test PNG export
    result = await agent.export_diagram(sample_data, "png", "demo")
    if result["success"]:
        print("✅ PNG export successful!")
    else:
        print(f"❌ PNG export failed: {result['error']}")

async def main():
    """Run all demos"""
    print("🎯 MindMapDiagramAgent Demo")
    print("=" * 50)
    
    try:
        await demo_mindmap()
        await demo_flowchart()
        await demo_orgchart()
        await demo_network()
        await demo_export()
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n💡 To use the web interface:")
        print("   python server.py")
        print("   Then open http://127.0.0.1:8030 in your browser")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure you have set up your OpenAI API key in the .env file")

if __name__ == "__main__":
    asyncio.run(main())
