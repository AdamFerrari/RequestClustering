import argparse
from cluster_analyzer import ClusterAnalyzer
from csv_handler import CSVHandler
from rich.console import Console
from rich.progress import Progress

def main():
    parser = argparse.ArgumentParser(description='Thematic clustering of CSV data using OpenAI API')
    parser.add_argument('csv_file', help='Path to the CSV file to analyze')
    parser.add_argument('--output', default='clusters.txt', help='Output file path (default: clusters.txt)')
    args = parser.parse_args()

    console = Console()

    try:
        # Initialize handlers
        csv_handler = CSVHandler(args.csv_file)
        analyzer = ClusterAnalyzer()

        # First pass: Generate clusters
        console.print("[bold blue]Phase 1: Generating clusters...[/]")
        rows = csv_handler.read_rows()
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing rows...", total=len(rows))
            
            for row in rows:
                analyzer.process_row_for_clusters(row)
                progress.update(task, advance=1)

        # Second pass: Assign rows to clusters
        console.print("\n[bold blue]Phase 2: Assigning rows to clusters...[/]")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Assigning clusters...", total=len(rows))
            
            for row in rows:
                analyzer.assign_row_to_cluster(row)
                progress.update(task, advance=1)

        # Output results
        clusters = analyzer.get_cluster_results()
        
        with open(args.output, 'w') as f:
            f.write("Thematic Clusters Analysis Results\n")
            f.write("=================================\n\n")
            
            for cluster_label, cluster_data in clusters.items():
                f.write(f"Cluster: {cluster_label}\n")
                f.write("-" * (len(cluster_label) + 9) + "\n")
                f.write(f"Number of items: {len(cluster_data)}\n")
                f.write("Row IDs: " + ", ".join(str(id) for id in cluster_data) + "\n\n")

        console.print(f"[bold green]Analysis complete! Results written to {args.output}[/]")

    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/]")
        exit(1)

if __name__ == "__main__":
    main()
