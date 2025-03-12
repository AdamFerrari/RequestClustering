import os
from openai import OpenAI
import json

class ClusterAnalyzer:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.clusters = {}  # cluster_label -> [row_ids]
        self.cluster_labels = set()

    def process_row_for_clusters(self, row):
        """First pass: Generate potential clusters for a row."""
        prompt = self._create_cluster_generation_prompt(row)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a thematic clustering expert. Analyze the content and suggest appropriate cluster labels."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            new_clusters = result.get("suggested_clusters", [])
            
            # Update cluster labels
            self.cluster_labels.update(new_clusters)
            
        except Exception as e:
            raise Exception(f"Failed to process row for clustering: {e}")

    def assign_row_to_cluster(self, row):
        """Second pass: Assign a row to the best matching cluster."""
        prompt = self._create_cluster_assignment_prompt(row)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a thematic clustering expert. Assign the content to the most appropriate existing cluster."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            assigned_cluster = result.get("assigned_cluster")
            
            if assigned_cluster:
                if assigned_cluster not in self.clusters:
                    self.clusters[assigned_cluster] = []
                self.clusters[assigned_cluster].append(row["id"])
                
        except Exception as e:
            raise Exception(f"Failed to assign row to cluster: {e}")

    def _create_cluster_generation_prompt(self, row):
        return f"""
Analyze the following content and suggest potential thematic clusters.
If the content fits existing clusters, prefer using them.

Title: {row['title']}
Description: {row['description']}

Existing clusters: {list(self.cluster_labels)}

Respond with JSON in this format:
{{
    "suggested_clusters": ["cluster1", "cluster2"]
}}

Keep cluster labels concise but descriptive.
"""

    def _create_cluster_assignment_prompt(self, row):
        return f"""
Assign the following content to the most appropriate existing cluster.

Title: {row['title']}
Description: {row['description']}

Available clusters: {list(self.cluster_labels)}

Respond with JSON in this format:
{{
    "assigned_cluster": "chosen_cluster_name"
}}

Choose exactly one best-fitting cluster.
"""

    def get_cluster_results(self):
        """Return the final clustering results."""
        return self.clusters
