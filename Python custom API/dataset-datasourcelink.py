#code sanitized to exclude company sensitive data

import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
import asyncio
import os
import pandas as pd
import time
import math

semaphore = asyncio.Semaphore(2)  # Limit to  concurrent requests
datasource_url_template = "https://api.powerbi.com/v1.0/myorg/admin/datasets/{dataset_id}/datasources"

db_username = os.environ.get('DB_USER')
username = db_username.split('@')[0]
year = 2024 #change to extract datasources information corresponding to that year
months_to_process = range(1, 4)

auth_url = 'https://login.microsoftonline.com/common/oauth2/token'

async def fetch_datasources(session, dataset_id, headers):
    datasource_url = datasource_url_template.format(dataset_id=dataset_id)
    async with semaphore:
        try:
            async with session.get(datasource_url, headers=headers) as response:
                if response.status == 404:
                    return {}  # Return an empty dictionary for 404 without printing anything
                response.raise_for_status()  # Raise an error for other bad responses
                return await response.json()
        except Exception as e:
            print(f"Error fetching datasources for dataset ID {dataset_id}: {e}")
            return {}

async def main():
    auth_parameters = {
        'client_id': '"<client_id>"', 
        'client_secret': '<client_secret>',
        'grant_type': 'password', 
        'resource': 'https://analysis.windows.net/powerbi/api', 
        'username': db_username,
        'password': os.environ.get('DB_PASSWORD'), 
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    timeout = aiohttp.ClientTimeout(total=60)  # Set total timeout to 30 seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Get the access token
        async with session.post(auth_url, data=auth_parameters) as token_response:
            token_response.raise_for_status()  # Raise an error for bad responses
            token = await token_response.json()
            access_token = token['access_token']
            general_headers = {'Authorization': f'Bearer {access_token}', 'Content-type': 'application/json; charset=utf-8'}

        retry_options = ExponentialRetry(attempts=3)
        async with RetryClient(session, retry_options=retry_options) as retry_client:

            # Fetch datasets
            dataset_ids_df = pd.read_csv(f'C://Users//{username}//OneDrive - Wolfspeed//Gateway Project//datasets_{year}.csv')  
            dataset_ids = dataset_ids_df['id'].tolist()  # Extract dataset IDs into a list
            data_for_df = []

            # Batching starts here
            BATCH_SIZE = 300
            WAIT_TIME = 3600  # seconds

            total_batches = math.ceil(len(dataset_ids) / BATCH_SIZE)
            for batch_num in range(total_batches):
                start = batch_num * BATCH_SIZE
                end = start + BATCH_SIZE
                batch_ids = dataset_ids[start:end]
                print(f"Processing batch {batch_num+1} of {total_batches}...")

                # Create a list of tasks for fetching datasources
                tasks = [
                        fetch_datasources(session, dataset_id, general_headers)
                        for dataset_id in batch_ids
                    ]

                # Gather all datasource responses
                datasource_responses = await asyncio.gather(*tasks)

                # Process the responses
                for dataset_id, datasource_response in zip(batch_ids, datasource_responses):
                    datasources = datasource_response.get('value', [])
                    datasource_id = [ds.get('datasourceId') for ds in datasources if ds.get('datasourceId') is not None]
                    if datasource_id:  # Only append if there are datasource IDs
                        data_for_df.append({
                            "Dataset ID": dataset_id,
                            "Data Sources": datasource_id
                        })

                if batch_num < total_batches - 1:
                        print("Waiting 1 hour for API call limit reset...")
                        await asyncio.sleep(WAIT_TIME)

            # Create the DataFrame
            df = pd.DataFrame(data_for_df)

            out_path = f"C://Users//{username}//OneDrive//Project//dataset-datasource_{year}.xlsx"
            # Use the context manager to handle the ExcelWriter
            with pd.ExcelWriter(out_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)  # Set index=False to avoid writing row indices

            print(f"DataFrame saved to {out_path}")

# Run the main function
asyncio.run(main())