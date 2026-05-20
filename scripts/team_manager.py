#!/usr/bin/env python3
import os
import sys
import json
import re
import shutil
import argparse

def load_claude_config():
    config = {
        "spec_save_path": "docs/spec.md",
        "plan_save_path": "teams/{team-name}/plan.md",
        "default_roles": ["fe", "be"],
        "testing_strategy": "manual",
        "create_docs": True,
        "auto_approve_dev_to_qa": False,
        "auto_approve_qa_to_docs": False,
        "cleanup_on_done": False
    }
    if not os.path.exists("CLAUDE.md"):
        return config
    
    try:
        with open("CLAUDE.md", "r") as f:
            content = f.read()
        
        match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
        if not match:
            return config
        
        yaml_text = match.group(1)
        current_key = None
        for line in yaml_text.splitlines():
            line_strip = line.strip()
            if not line_strip or line_strip.startswith("#"):
                continue
            
            is_sub = line.startswith(" ") or line.startswith("\t")
            
            if ":" in line_strip:
                key, val = line_strip.split(":", 1)
                key = key.strip()
                val = val.split("#")[0].strip()
                
                # Simple type conversions
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                elif val.startswith("[") and val.endswith("]"):
                    val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                
                if is_sub and current_key:
                    if current_key == "spec":
                        if key == "save_path": config["spec_save_path"] = val
                        elif key == "auto_plan": config["spec_auto_plan"] = val
                    elif current_key == "plan":
                        if key == "save_path": config["plan_save_path"] = val
                    elif current_key == "feature_team":
                        if key == "default_roles": config["default_roles"] = val
                        elif key == "testing_strategy": config["testing_strategy"] = val
                        elif key == "create_docs": config["create_docs"] = val
                        elif key == "auto_approve_dev_to_qa": config["auto_approve_dev_to_qa"] = val
                        elif key == "auto_approve_qa_to_docs": config["auto_approve_qa_to_docs"] = val
                        elif key == "cleanup_on_done": config["cleanup_on_done"] = val
                else:
                    current_key = key
    except Exception as e:
        print(f"Warning: Failed to parse CLAUDE.md config: {e}", file=sys.stderr)
        
    return config

def get_team_dir(team_name):
    return os.path.join("teams", team_name)

def get_config_path(team_name):
    return os.path.join(get_team_dir(team_name), "config.json")

def get_plan_path(team_name, config_data=None):
    global_config = load_claude_config()
    raw_path = global_config["plan_save_path"]
    return raw_path.replace("{team-name}", team_name)

def load_team_config(team_name):
    path = get_config_path(team_name)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_team_config(team_name, config_data):
    path = get_config_path(team_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(config_data, f, indent=2)

def init_team(team_name, required_roles=None):
    global_config = load_claude_config()
    if not required_roles:
        required_roles = global_config["default_roles"]
    
    # Always include docs and qa in the team's potential pool unless config/args override
    all_roles = list(required_roles)
    if "qa" not in all_roles and global_config["testing_strategy"] != "manual":
        all_roles.append("qa")
    if "docs" not in all_roles and global_config["create_docs"]:
        all_roles.append("docs")
        
    team_dir = get_team_dir(team_name)
    os.makedirs(team_dir, exist_ok=True)
    
    # Scaffolding inboxes
    inboxes_dir = os.path.join(team_dir, "inboxes")
    for role in all_roles:
        os.makedirs(os.path.join(inboxes_dir, role), exist_ok=True)
        # Create empty mailbox file
        with open(os.path.join(inboxes_dir, role, "mailbox.md"), "w") as f:
            f.write(f"# Mailbox for {role.upper()}\n\nNo messages yet.\n")
            
    # Initial runtime config
    config_data = {
        "team_name": team_name,
        "phase": "PLANNING",
        "required_roles": required_roles, # only the ones assigned for dev/arch initially
        "all_roles": all_roles,
        "active_agents": [],
        "completed_agents": [],
        "history": []
    }
    save_team_config(team_name, config_data)
    
    # Initialize plan.md if not exists
    plan_path = get_plan_path(team_name)
    os.makedirs(os.path.dirname(plan_path), exist_ok=True)
    
    if not os.path.exists(plan_path):
        with open(plan_path, "w") as f:
            f.write(f"# Plan: {team_name}\n\n")
            f.write("## Roles Assigned\n")
            for r in required_roles:
                f.write(f"- {r.upper()}\n")
            f.write("\n")
            
            # Add headings per role
            role_headings = {
                "architecture": "Architecture Tasks",
                "fe": "Frontend Tasks",
                "be": "Backend Tasks",
                "qa": "QA Tasks",
                "docs": "Documentation Tasks"
            }
            for role in all_roles:
                heading = role_headings.get(role, f"{role.upper()} Tasks")
                f.write(f"## {heading}\n")
                f.write(f"- [ ] Task: Set up core {role.upper()} boundaries\n")
                f.write(f"  Acceptance: Core requirements configured\n")
                f.write(f"  Verify: Verify setup\n")
                f.write(f"  Files: []\n\n")
                
    print(f"Successfully initialized team '{team_name}' in {team_dir}")
    print(f"Scaffolded inboxes: {', '.join(all_roles)}")
    print(f"Plan file created: {plan_path}")

def parse_tasks(plan_path):
    if not os.path.exists(plan_path):
        return {}
        
    with open(plan_path, "r") as f:
        content = f.read()
        
    role_headings = {
        "Architecture Tasks": "architecture",
        "Frontend Tasks": "fe",
        "Backend Tasks": "be",
        "QA Tasks": "qa",
        "Documentation Tasks": "docs"
    }
    
    tasks = {}
    current_role = None
    
    lines = content.splitlines()
    for line in lines:
        if line.startswith("## "):
            heading = line[3:].strip()
            current_role = role_headings.get(heading, None)
            if current_role:
                tasks[current_role] = []
        elif line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
            if current_role:
                checked = line.strip().startswith("- [x]")
                task_desc = line.split("]", 1)[1].strip()
                tasks[current_role].append({"desc": task_desc, "completed": checked})
                
    return tasks

def print_status(team_name):
    config_data = load_team_config(team_name)
    if not config_data:
        print(f"Error: Team '{team_name}' is not initialized.", file=sys.stderr)
        return
        
    plan_path = get_plan_path(team_name)
    tasks = parse_tasks(plan_path)
    
    print("====================================================")
    print(f" TEAM STATUS: {config_data['team_name'].upper()}")
    print(f" Current Phase: {config_data['phase']}")
    print("====================================================")
    
    for role in config_data["all_roles"]:
        role_tasks = tasks.get(role, [])
        role_status = "IDLE"
        if role in config_data["active_agents"]:
            role_status = "ACTIVE 🚀"
        elif role in config_data["completed_agents"]:
            role_status = "COMPLETED ✅"
            
        print(f"\nRole: {role.upper()} ({role_status})")
        if not role_tasks:
            print("  No tasks defined.")
        else:
            for task in role_tasks:
                status_icon = "[x]" if task["completed"] else "[ ]"
                print(f"  {status_icon} {task['desc']}")
                
    print("\n====================================================")
    
    # Check if we are waiting for user action
    phase = config_data["phase"]
    if phase == "PLANNING":
        print("Status: Waiting for user approval on spec / planning details.")
        print(f"To start development, run: python3 scripts/team_manager.py approve {team_name}")
    elif phase == "DEV":
        # Check if all dev tasks are complete
        dev_roles = [r for r in config_data["required_roles"] if r not in ["qa", "docs"]]
        all_done = True
        for role in dev_roles:
            for t in tasks.get(role, []):
                if not t["completed"]:
                    all_done = False
                    
        if all_done:
            print("Status: All development tasks COMPLETED. Waiting for user approval to proceed to QA.")
            print(f"To approve and proceed to QA, run: python3 scripts/team_manager.py approve {team_name}")
        else:
            print("Status: Development is currently IN PROGRESS. Spawned dev agents are working.")
    elif phase == "QA":
        qa_done = True
        for t in tasks.get("qa", []):
            if not t["completed"]:
                qa_done = False
                
        if qa_done:
            print("Status: QA testing tasks COMPLETED. Waiting for user approval to proceed to Docs.")
            print(f"To approve and proceed to Docs, run: python3 scripts/team_manager.py approve {team_name}")
        else:
            print("Status: QA testing is currently IN PROGRESS.")
    elif phase == "DOCS":
        docs_done = True
        for t in tasks.get("docs", []):
            if not t["completed"]:
                docs_done = False
                
        if docs_done:
            print("Status: Documentation tasks COMPLETED. Ready to close feature team.")
            print(f"To finalize and clean up, run: python3 scripts/team_manager.py approve {team_name}")
        else:
            print("Status: Documentation is currently IN PROGRESS.")

def write_mailbox(team_name, role, subject, body):
    mailbox_path = os.path.join(get_team_dir(team_name), "inboxes", role, "mailbox.md")
    os.makedirs(os.path.dirname(mailbox_path), exist_ok=True)
    with open(mailbox_path, "a") as f:
        f.write(f"\n## {subject}\n\n{body}\n\n---\n")

def approve_phase(team_name):
    config_data = load_team_config(team_name)
    if not config_data:
        print(f"Error: Team '{team_name}' is not initialized.", file=sys.stderr)
        return
        
    global_config = load_claude_config()
    phase = config_data["phase"]
    
    if phase == "PLANNING":
        # Transition to DEV
        config_data["phase"] = "DEV"
        config_data["active_agents"] = [r for r in config_data["required_roles"] if r not in ["qa", "docs"]]
        save_team_config(team_name, config_data)
        
        # Brief dev agents
        for role in config_data["active_agents"]:
            write_mailbox(
                team_name, role, 
                "Phase Started: DEVELOPMENT", 
                f"You have been spawned for feature development. Please read your guidelines in `agents/{role}.md` and complete all tasks assigned to you under '## {role.upper()} Tasks' in your team plan."
            )
        print(f"Phase transitioned to DEV. Active dev agents: {', '.join(config_data['active_agents'])}")
        
    elif phase == "DEV":
        # Dev completed -> proceed to QA (or bypass to Docs/Completed if QA skipped)
        config_data["completed_agents"].extend(config_data["active_agents"])
        config_data["active_agents"] = []
        
        # Determine next phase
        has_qa = "qa" in config_data["all_roles"] and global_config["testing_strategy"] != "manual"
        
        if has_qa:
            config_data["phase"] = "QA"
            config_data["active_agents"] = ["qa"]
            save_team_config(team_name, config_data)
            write_mailbox(
                team_name, "qa",
                "Phase Started: QA TESTING",
                f"Development is complete. Please verify the implementation using testing strategy: {global_config['testing_strategy']}. Check off tasks under '## QA Tasks' when complete."
            )
            print("Phase transitioned to QA. Spawned QA agent.")
            
            # If auto-approve is true, immediately transition again
            if global_config["auto_approve_dev_to_qa"]:
                print("Auto-approving QA phase...")
                # Mock QA tasks completed
                plan_path = get_plan_path(team_name)
                complete_all_role_tasks(plan_path, "QA Tasks")
                approve_phase(team_name)
        else:
            # Skip QA, go to Docs
            print("Skipping QA phase (configured for manual or skipped). Proceeding to Docs...")
            config_data["phase"] = "QA" # temporary transition to handle downstream flow
            save_team_config(team_name, config_data)
            approve_phase(team_name)
            
    elif phase == "QA":
        # QA completed -> proceed to DOCS
        if "qa" in config_data["active_agents"]:
            config_data["completed_agents"].append("qa")
            config_data["active_agents"] = []
            
        has_docs = "docs" in config_data["all_roles"] and global_config["create_docs"]
        
        if has_docs:
            config_data["phase"] = "DOCS"
            config_data["active_agents"] = ["docs"]
            save_team_config(team_name, config_data)
            write_mailbox(
                team_name, "docs",
                "Phase Started: DOCUMENTATION",
                "QA testing is complete. Please review the implementation diffs and update project docs. Generate the changelog, then mark tasks under '## Documentation Tasks' complete."
            )
            print("Phase transitioned to DOCS. Spawned Docs agent.")
            
            # If auto-approve is true, immediately transition again
            if global_config["auto_approve_qa_to_docs"]:
                print("Auto-approving Docs phase...")
                plan_path = get_plan_path(team_name)
                complete_all_role_tasks(plan_path, "Documentation Tasks")
                approve_phase(team_name)
        else:
            print("Skipping Docs phase. Finalizing team...")
            config_data["phase"] = "DOCS"
            save_team_config(team_name, config_data)
            approve_phase(team_name)
            
    elif phase == "DOCS":
        # Docs completed -> finalize
        if "docs" in config_data["active_agents"]:
            config_data["completed_agents"].append("docs")
            config_data["active_agents"] = []
            
        config_data["phase"] = "COMPLETED"
        save_team_config(team_name, config_data)
        
        # Write changelog
        changelog_dir = os.path.join("docs", "changelogs")
        os.makedirs(changelog_dir, exist_ok=True)
        changelog_path = os.path.join(changelog_dir, f"{team_name}.md")
        
        plan_path = get_plan_path(team_name)
        tasks = parse_tasks(plan_path)
        
        with open(changelog_path, "w") as f:
            f.write(f"# Feature Changelog: {team_name}\n\n")
            f.write("## Phase Completion Summary\n")
            f.write("- **Development**: Completed successfully.\n")
            if "qa" in config_data["completed_agents"]:
                f.write("- **QA & Testing**: Passed verification.\n")
            if "docs" in config_data["completed_agents"]:
                f.write("- **Documentation**: Updated.\n")
            f.write("\n## Completed Tasks\n")
            for role, r_tasks in tasks.items():
                f.write(f"\n### {role.upper()}\n")
                for t in r_tasks:
                    f.write(f"- [x] {t['desc']}\n")
                    
        print(f"Feature team execution completed! Changelog saved to: {changelog_path}")
        
        if global_config["cleanup_on_done"]:
            clean_team(team_name)
        else:
            print("Cleanup skipped (configured to keep team directory).")

def complete_all_role_tasks(plan_path, heading_text):
    if not os.path.exists(plan_path):
        return
    with open(plan_path, "r") as f:
        content = f.read()
    
    # Toggle all task boxes under heading_text
    lines = content.splitlines()
    new_lines = []
    under_heading = False
    for line in lines:
        if line.startswith("## "):
            under_heading = (line[3:].strip() == heading_text)
        elif line.startswith("##") and not line.startswith("## "):
            under_heading = False # nested heading
            
        if under_heading and line.strip().startswith("- [ ]"):
            line = line.replace("- [ ]", "- [x]", 1)
        new_lines.append(line)
        
    with open(plan_path, "w") as f:
        f.write("\n".join(new_lines) + "\n")

def clean_team(team_name):
    team_dir = get_team_dir(team_name)
    if os.path.exists(team_dir):
        shutil.rmtree(team_dir)
        print(f"Successfully cleaned up and deleted team directory: {team_dir}")
    else:
        print(f"Team directory {team_dir} does not exist.")

def main():
    parser = argparse.ArgumentParser(description="Feature Team Scaffolding and Status Script")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    init_parser = subparsers.add_parser("init", help="Initialize a new feature team workspace")
    init_parser.add_argument("team_name", help="Name of the team/feature")
    init_parser.add_argument("roles", nargs="*", help="Optional roles (e.g., fe be architecture)")
    
    status_parser = subparsers.add_parser("status", help="Get feature team status")
    status_parser.add_argument("team_name", help="Name of the team/feature")
    
    approve_parser = subparsers.add_parser("approve", help="Approve current phase gate and proceed")
    approve_parser.add_argument("team_name", help="Name of the team/feature")
    
    clean_parser = subparsers.add_parser("clean", help="Cleanup and teardown a team workspace")
    clean_parser.add_argument("team_name", help="Name of the team/feature")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_team(args.team_name, args.roles if args.roles else None)
    elif args.command == "status":
        print_status(args.team_name)
    elif args.command == "approve":
        approve_phase(args.team_name)
    elif args.command == "clean":
        clean_team(args.team_name)

if __name__ == "__main__":
    main()
