from src.client_factory import RDSClient
from src.rds import RDS

def deploy_resources():
    rds_client = RDSClient().get_client()
    rds = RDS(rds_client)

    rds.create_postgresql_instance()

    print("Creating RDS PostgreSQL Instance...")

if __name__ == '__main__':
    deploy_resources()