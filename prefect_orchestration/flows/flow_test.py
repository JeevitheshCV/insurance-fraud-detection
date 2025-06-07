from prefect import flow

@flow(name="test-flow")
def my_first_flow():
    print("✅ Prefect flow executed successfully!")

if __name__ == "__main__":
    my_first_flow()
