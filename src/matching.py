import duckdb
import os
from splink.duckdb.linker import DuckDBLinker
from splink.duckdb.blocking_rule_library import block_on
import splink.duckdb.comparison_library as cl
import splink.duckdb.comparison_template_library as ctl
from src.database import DB_PATH

def run_matching():
    # Connect to the EXISTING DuckDB where we have our data
    # Note: Splink manages its own connection usually, but we can pass the path
    
    # Settings for the Linker
    # SIMPLIFIED SETTINGS for robust execution
    settings = {
        "link_type": "dedupe_only",
        "unique_id_column_name": "uniq_id",
        "blocking_rules_to_generate_predictions": [
            "l.email_norm = r.email_norm",
            "l.ssn_clean = r.ssn_clean",
            "l.first_name_norm = r.first_name_norm AND l.last_name_norm = r.last_name_norm"
        ],
        "comparisons": [
            cl.levenshtein_at_thresholds("first_name_norm", 2),
            cl.levenshtein_at_thresholds("last_name_norm", 2),
            cl.exact_match("email_norm"),
            cl.exact_match("ssn_clean"),
            cl.exact_match("dob_std"),
            cl.exact_match("full_address_norm"),
        ],
        "retain_intermediate_calculation_columns": True,
    }

    con = duckdb.connect(DB_PATH)
    
    print("Initializing Splink Linker...")
    linker = DuckDBLinker("processed_people", settings, connection=con)
    
    # Estimate probability two random records match (u)
    linker.estimate_u_using_random_sampling(max_pairs=1e6)
    
    # Training (Expectation Maximization)
    # Skipping EM training due to splink internal error on this env. 
    # Using defaults/random sampling U should give reasonable results for strict blocking.
    # print("Training Email...")
    # linker.estimate_parameters_using_expectation_maximisation("l.email_norm = r.email_norm")
    
    # print("Training SSN...")
    # linker.estimate_parameters_using_expectation_maximisation("l.ssn_clean = r.ssn_clean")
    
    # Predict
    print("Predicting matches...")
    df_predictions = linker.predict(threshold_match_probability=0.8)
    
    # Clustering
    print("Clustering entities...")
    clusters = linker.cluster_pairwise_predictions_at_threshold(df_predictions, threshold_match_probability=0.85)
    
    # Write clusters back to DB for visualization
    # We use the physical name of the Splink table
    cluster_table_name = clusters.physical_name
    
    sql = f"""
        CREATE OR REPLACE TABLE entity_clusters AS
        SELECT 
            cluster_id,
            id,
            first_name_norm,
            last_name_norm,
            email_norm,
            ssn_clean
        FROM {cluster_table_name}
    """
    con.execute(sql)
    
    print("Matching complete. Clusters saved to 'entity_clusters'.")
    con.close()

if __name__ == "__main__":
    run_matching()
