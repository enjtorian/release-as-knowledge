#!/usr/bin/env python3
import os
import json
import sys
import subprocess
import argparse
import uuid
from datetime import datetime

def install_dependencies():
    """Install required dependencies."""
    print("Checking dependencies...")
    try:
        import yaml
        import jsonschema
        print("Dependencies are already installed.")
    except ImportError:
        print("Missing dependencies. Installing PyYAML and jsonschema...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML", "jsonschema"])
        print("Dependencies installed successfully.")

def load_schema(schema_path):
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

def do_validate(args):
    """Validate all YAML tasks against the schema."""
    try:
        import yaml
        from jsonschema import validate, ValidationError
    except ImportError:
        print("Error: PyYAML and jsonschema are required. Run with --install to install them.")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    list_dir = os.path.join(base_dir, "list")
    schema_path = os.path.join(base_dir, "task.schema.json")

    schema = load_schema(schema_path)

    success_count = 0
    error_count = 0

    print(f"Validating YAML files in {list_dir}...")

    for root, dirs, files in os.walk(list_dir):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_dir)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    
                    if data is None:
                        continue
                        
                    validate(instance=data, schema=schema)
                    
                    # Check record_path existence if it is defined
                    if "record_path" in data:
                         record_full_path = os.path.join(os.path.dirname(file_path), data["record_path"])
                         if not os.path.exists(record_full_path):
                             print(f"[WARNING] {relative_path}: Record file defined but not found at {data['record_path']}")

                    print(f"[OK] {relative_path}")
                    success_count += 1
                except yaml.YAMLError as e:
                    print(f"[YAML ERROR] {relative_path}: {e}")
                    error_count += 1
                except ValidationError as e:
                    print(f"[SCHEMA ERROR] {relative_path}: {e.message}")
                    error_count += 1
                except Exception as e:
                    print(f"[UNKNOWN ERROR] {relative_path}: {e}")
                    error_count += 1

    print("\nValidation Summary:")
    print(f"  Total Valid: {success_count}")
    print(f"  Total Errors: {error_count}")

    if error_count > 0:
        sys.exit(1)

def do_init(args):
    """Initialize POG structure."""
    base_dir = os.getcwd()
    pog_dir = os.path.join(base_dir, "pog-task")
    list_dir = os.path.join(pog_dir, "list")

    if os.path.exists(pog_dir):
        print(f"POG structure already exists at {pog_dir}")
        return

    os.makedirs(list_dir, exist_ok=True)
    print(f"Created {pog_dir}")
    print(f"Created {list_dir}")
    # TODO: Create standard README and Schema? 

def do_status(args):
    """List active tasks."""
    try:
        import yaml
    except ImportError:
         print("Error: PyYAML is required.")
         sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    list_dir = os.path.join(base_dir, "list")
    
    print(f"{'ID':<38} {'STATUS':<12} {'TITLE'}")
    print("-" * 80)

    for root, dirs, files in os.walk(list_dir):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if data and data.get("status") in ["in_progress", "in_review", "blocked"]:
                            print(f"{data.get('id', 'N/A'):<38} {data.get('status', 'N/A'):<12} {data.get('title', 'N/A')}")
                except Exception:
                    pass

def do_new(args):
    """Interactively create a new task."""
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML is required.")
        sys.exit(1)

    print("Creating a new POG Task...")
    title = input("Task Title: ").strip()
    if not title:
        print("Title is required.")
        return

    project = input("Project (default: common): ").strip() or "common"
    module = input("Module (default: core): ").strip() or "core"
    
    category = input("Category (feature/bugfix/doc/etc) [doc]: ").strip() or "doc"
    priority = input("Priority (low/medium/high) [medium]: ").strip() or "medium"
    
    task_id = str(uuid.uuid4())
    now = datetime.now().astimezone().isoformat()
    
    task_data = {
        "type": "task",
        "id": task_id,
        "title": title,
        "description": "",
        "category": category,
        "priority": priority,
        "status": "pending",
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "estimated_hours": 1,
        "actual_hours": 0,
        "claimed_by": None,
        "claimed_at": None,
        "related_files": [],
        "dependencies": [],
        "blocking": [],
        "tags": [],
        "checklist": [],
        "parent_task": None,
        "notes": "",
        "history": [
            {
                "timestamp": now,
                "agent": "pog-cli",
                "action": "created",
                "message": "Task created via CLI"
            }
        ],
        "record_path": f"record/{task_id}/record.md"
    }
    
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    task_dir = os.path.join(base_dir, "list", project, module)
    os.makedirs(task_dir, exist_ok=True)
    
    # Create valid filename from title
    safe_title = "".join([c if c.isalnum() else "_" for c in title])
    yaml_filename = f"{safe_title}.yaml"
    yaml_path = os.path.join(task_dir, yaml_filename)
    
    # Create record directory
    record_dir = os.path.join(task_dir, "record", task_id)
    os.makedirs(record_dir, exist_ok=True)
    record_path = os.path.join(record_dir, "record.md")
    
    # Write YAML
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f, allow_unicode=True, sort_keys=False)
        
    # Write Record
    with open(record_path, "w", encoding="utf-8") as f:
        f.write(f"# Task Record: {title}\n\n- **Task UUID**: `{task_id}`\n- **Status**: Pending\n\n## Goal\n\n## Execution Plan\n- [ ] ...\n")
        
    print(f"\nTask created successfully!")
    print(f"YAML: {os.path.relpath(yaml_path, base_dir)}")
    print(f"Record: {os.path.relpath(record_path, base_dir)}")

def main():
    parser = argparse.ArgumentParser(description="POG Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # install
    parser_install = subparsers.add_parser("install", help="Install dependencies")

    # init
    parser_init = subparsers.add_parser("init", help="Initialize POG structure")

    # validate
    parser_validate = subparsers.add_parser("validate", help="Validate all tasks")

    # status
    parser_status = subparsers.add_parser("status", help="List active tasks")
    
    # new
    parser_new = subparsers.add_parser("new", help="Create a new task")

    args = parser.parse_args()

    if args.command == "install":
        install_dependencies()
    elif args.command == "init":
        do_init(args)
    elif args.command == "validate":
        do_validate(args)
    elif args.command == "status":
        do_status(args)
    elif args.command == "new":
        do_new(args)
    else:
        # Default to validate for backward compatibility if no args, or print help
        if len(sys.argv) == 1:
            do_validate(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
