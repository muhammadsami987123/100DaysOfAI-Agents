#!/usr/bin/env python3
"""
CLI interface for GPTConfigGenerator
"""

import argparse
import sys
import json
from typing import Optional
from agent import GPTConfigGenerator

def main():
    parser = argparse.ArgumentParser(
        description="GPTConfigGenerator - Generate configuration files from natural language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "Create a JSON config for Express app with port 3000"
  python cli.py "Generate docker-compose.yml with PostgreSQL and Redis" --format yaml
  python cli.py --explain config.json --format json
  python cli.py --convert config.json --from json --to yaml
        """
    )
    
    # Main command group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "request",
        nargs="?",
        help="Natural language description of the configuration you want to generate"
    )
    group.add_argument(
        "--explain",
        metavar="FILE",
        help="Explain an existing configuration file"
    )
    group.add_argument(
        "--convert",
        metavar="FILE",
        help="Convert a configuration file to another format"
    )
    group.add_argument(
        "--validate",
        metavar="FILE",
        help="Validate a configuration file"
    )
    
    # Options
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "toml", "js", "ts"],
        default="json",
        help="Output format for generated configuration (default: json)"
    )
    
    parser.add_argument(
        "--type",
        choices=["auto", "app_settings", "devops", "linting", "build_tools", "package_managers", "database", "custom"],
        default="auto",
        help="Configuration type (default: auto-detect)"
    )
    
    parser.add_argument(
        "--from",
        dest="from_format",
        choices=["json", "yaml", "toml", "js", "ts"],
        help="Source format for conversion (required with --convert)"
    )
    
    parser.add_argument(
        "--to",
        dest="to_format",
        choices=["json", "yaml", "toml", "js", "ts"],
        help="Target format for conversion (required with --convert)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    try:
        agent = GPTConfigGenerator()
    except Exception as e:
        print(f"Error initializing agent: {e}", file=sys.stderr)
        print("Make sure you have set up your API keys in the .env file", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.request:
            # Generate configuration
            result = agent.generate_config(
                user_request=args.request,
                config_type=args.type,
                format=args.format
            )
            
            if result["success"]:
                output = result["config_content"]
                if args.verbose:
                    print(f"Generated {args.format.upper()} configuration:", file=sys.stderr)
                    print(f"Type: {result.get('detected_type', 'auto')}", file=sys.stderr)
                    print("-" * 50, file=sys.stderr)
                
                write_output(output, args.output)
                
                if args.verbose:
                    print("-" * 50, file=sys.stderr)
                    print("Configuration generated successfully!", file=sys.stderr)
            else:
                print(f"Error generating configuration: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
                
        elif args.explain:
            # Explain configuration
            try:
                with open(args.explain, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.explain}' not found", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
            
            result = agent.explain_config(content, args.format)
            
            if result["success"]:
                output = result["explanation"]
                if args.verbose:
                    print(f"Explanation of {args.format.upper()} configuration:", file=sys.stderr)
                    print("-" * 50, file=sys.stderr)
                
                write_output(output, args.output)
            else:
                print(f"Error explaining configuration: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
                
        elif args.convert:
            # Convert configuration
            if not args.from_format or not args.to_format:
                print("Error: --from and --to formats are required for conversion", file=sys.stderr)
                sys.exit(1)
            
            try:
                with open(args.convert, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.convert}' not found", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
            
            result = agent.convert_config(content, args.from_format, args.to_format)
            
            if result["success"]:
                output = result["converted_content"]
                if args.verbose:
                    print(f"Converted {args.from_format.upper()} to {args.to_format.upper()}:", file=sys.stderr)
                    print("-" * 50, file=sys.stderr)
                
                write_output(output, args.output)
            else:
                print(f"Error converting configuration: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
                
        elif args.validate:
            # Validate configuration
            try:
                with open(args.validate, 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.validate}' not found", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
            
            result = agent.validate_config(content, args.format)
            
            if result["valid"]:
                print("✅ Configuration is valid", file=sys.stderr)
                if args.verbose:
                    print(f"Format: {result['format']}", file=sys.stderr)
                    print(f"Parsed configuration: {json.dumps(result['parsed_config'], indent=2)}", file=sys.stderr)
                sys.exit(0)
            else:
                print(f"❌ Configuration is invalid: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def write_output(content: str, output_file: Optional[str]):
    """Write content to file or stdout"""
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(content)
            print(f"Output written to {output_file}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(content)

if __name__ == "__main__":
    main()
