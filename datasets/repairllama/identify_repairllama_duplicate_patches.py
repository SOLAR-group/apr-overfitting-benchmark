import os
import re
from collections import defaultdict

def get_normalized_patch(filepath):
    """
    Reads a patch file and removes the 'index ...' line.
    Also strips trailing whitespaces and normalizes line endings, 
    which are common invisible differences in LLM-generated files.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    normalized = []
    for line in lines:
        if line.startswith('index '):
            continue
        # rstrip() removes trailing spaces, tabs, \r, and \n
        normalized.append(line.rstrip())
        
    return '\n'.join(normalized)

def main():
    # Set the base directory path
    current_dir = os.getcwd()
    
    base_dir = os.path.join(
        current_dir, 
        "datasets", 
        "repairllama", 
        "context_size_3_filtered"
    )
    correct_dir = os.path.join(base_dir, "correct")
    overfitting_dir = os.path.join(base_dir, "overfitting")
    
    # Dictionary to hold files: { "Chart_1": {"correct": [...], "overfitting": [...]} }
    bugs = defaultdict(lambda: {'correct': [], 'overfitting': []})
    
    # Regex to extract the BugID (e.g., 'Chart_1') from the filename
    bug_id_pattern = re.compile(r'^([A-Za-z]+_\d+)_')
    
    # 1. Gather all file paths
    for category, directory in [('correct', correct_dir), ('overfitting', overfitting_dir)]:
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} does not exist. Skipping.")
            continue
            
        for filename in os.listdir(directory):
            if filename.endswith('.diff'):
                match = bug_id_pattern.match(filename)
                if match:
                    bug_id = match.group(1)
                    bugs[bug_id][category].append(os.path.join(directory, filename))

    # 2. Process and find duplicates
    all_duplicates = []  # List of tuples: (duplicate_file, original_file)
    total_original_patches = 0
    table_rows = []

    for bug_id, patches in bugs.items():
        seen_contents = {}  # Map of: normalized_content -> first_seen_filepath
        
        orig_corr = len(patches['correct'])
        orig_over = len(patches['overfitting'])
        orig_total = orig_corr + orig_over
        total_original_patches += orig_total

        dedup_corr = 0
        dedup_over = 0

        # Process 'correct' patches first
        for filepath in patches['correct']:
            content = get_normalized_patch(filepath)
            if content in seen_contents:
                all_duplicates.append((filepath, seen_contents[content]))
            else:
                seen_contents[content] = filepath
                dedup_corr += 1
                
        # Process 'overfitting' patches
        for filepath in patches['overfitting']:
            content = get_normalized_patch(filepath)
            if content in seen_contents:
                all_duplicates.append((filepath, seen_contents[content]))
            else:
                seen_contents[content] = filepath
                dedup_over += 1

        dedup_total = dedup_corr + dedup_over
        
        table_rows.append({
            'BugID': bug_id,
            'orig_corr': orig_corr,
            'orig_over': orig_over,
            'orig_total': orig_total,
            'dedup_corr': dedup_corr,
            'dedup_over': dedup_over,
            'dedup_total': dedup_total
        })

    # 3. Print Results
    total_duplicates = len(all_duplicates)
    total_dedup_patches = total_original_patches - total_duplicates
    
    print("="*80)
    print("DUPLICATE PATCHES LIST")
    print("="*80)
    if not all_duplicates:
        print("No duplicates found.")
    else:
        for dup, orig in all_duplicates:
            dup_name = os.path.basename(dup)
            orig_name = os.path.basename(orig)
            print(f"- '{dup_name}' is a duplicate of '{orig_name}'")

    print("\n" + "="*80)
    print("SUMMARY METRICS")
    print("="*80)
    print(f"Total Original Patches : {total_original_patches}")
    print(f"Total Duplicates Found : {total_duplicates}")
    print(f"Total Unique Patches   : {total_dedup_patches}")
    if total_original_patches > 0:
        dup_percentage = (total_duplicates / total_original_patches) * 100
        print(f"Duplication Rate       : {dup_percentage:.2f}%")

    print("\n" + "="*115)
    print(f"{'BugID':<15} | {'Orig. Correct':<13} | {'Orig. Overfit':<13} | {'Dedup Correct':<13} | {'Dedup Overfit':<13} | {'Orig. Total':<11} | {'Dedup Total':<11}")
    print("-" * 115)
    
    # Sort alphabetically by BugID for readability
    table_rows.sort(key=lambda x: x['BugID'])
    
    for row in table_rows:
        print(f"{row['BugID']:<15} | "
              f"{row['orig_corr']:<13} | "
              f"{row['orig_over']:<13} | "
              f"{row['dedup_corr']:<13} | "
              f"{row['dedup_over']:<13} | "
              f"{row['orig_total']:<11} | "
              f"{row['dedup_total']:<11}")
    print("="*115)

if __name__ == "__main__":
    main()