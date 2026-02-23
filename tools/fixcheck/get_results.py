import os
import csv
import argparse

def determine_actual_correctness(patch_name, patches_dir):
    """Determine actual correctness based on which subdirectory the patch is located in"""
    correct_path = os.path.join(patches_dir, "correct", f'{patch_name}.diff')
    overfitting_path = os.path.join(patches_dir, "overfitting", f'{patch_name}.diff')
    
    if os.path.exists(correct_path):
        return "correct"
    elif os.path.exists(overfitting_path):
        return "overfitting"
    else:
        # This is never executed in the current setup, but we keep it for safety
        print(f"Warning: {patch_name} not found in either correct or overfitting directories.")
        return "unknown"

def determine_prediction(assertion_failing_prefixes):
    """Determine prediction based on the values in the report.csv"""
    failing = int(assertion_failing_prefixes) if assertion_failing_prefixes else 0
    
    if failing > 0: 
        return "overfitting"
    else: #could not generate a failing assertion
        return "correct"

def process_directory(directory, method, patches_dir):
    """Process all subdirectories and collect results"""
    results = []
    
    # Walk through all subdirectories in the given directory
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        
        # Skip if not a directory
        if not os.path.isdir(subdir_path):
            continue
        
        # Check if the method directory exists and contains report.csv
        method_path = os.path.join(subdir_path, method)
        report_path = os.path.join(method_path, "report.csv")

        # For every compiled patch, check if fixcheck was able to generate a failing assertion which marks a patch as overfitting
        prediction = 'correct'

        correctness = determine_actual_correctness(subdir, patches_dir)
        if os.path.exists(report_path):
            try:
                with open(report_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    
                    # Get the first row
                    for row in reader:
                        assertion_failing_prefixes = row.get('assertion_failing_prefixes', '0')
                        
                        # Determine prediction
                        prediction = determine_prediction(assertion_failing_prefixes)
                                   
                        # We only need the first row
                        break
            except Exception as e:
                print(f"Error processing {report_path}: {e}")

        results.append({
                        'patch_name': f'{subdir}.diff',
                        'correctness': correctness,
                        'prediction': prediction
                        })
         
    return results

def main():
    parser = argparse.ArgumentParser(description="Process fixcheck results.")
    parser.add_argument('--results-dir', type=str, required=True, help='Relative path to the results directory, e.g. fixcheck-output/defects-repairing')
    parser.add_argument('--patches-dir', type=str, required=True, help='Relative path to the all patches used in experiment run, e.g. ../../datasets/petke/all_patches')
    parser.add_argument('--out', type=str, required=True, help='Output CSV filename, e.g. fixcheck_results_8h_test.csv')
    args = parser.parse_args()

    results = process_directory(args.results_dir, 'replit-code-llm', args.patches_dir)
    output_path = args.out

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['patch_name', 'correctness', 'prediction']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
