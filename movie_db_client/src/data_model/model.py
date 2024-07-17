from sqlalchemy import MetaData, Table
from repository.engine import engine
from tabulate import tabulate

metadata_obj = MetaData()

# Reflect all table at once
metadata_obj.reflect(bind=engine)


table_names = [k for k in metadata_obj.tables.keys() if k != "alembic_version"]


tables = {table_name: Table(table_name, metadata_obj, autoload_with=engine) for table_name in table_names}


def get_table_info(table: Table, copy_to_clipboard: bool = False) -> None:
    
    # Get primary key
    primary_key = table.primary_key.columns.keys()

    # Get foreign keys
    foreign_keys = [fk.target_fullname for fk in table.foreign_keys]

    # Get constraints
    constraints = [constraint.name for constraint in table.constraints]

    # Prepare column data for tabulation
    column_data = [
        [col.name, str(col.type), col.nullable, col.default] for col in table.columns
    ]

    # Prepare overall table data
    data = [
        ["Table", table.name],
        ["Columns", tabulate(column_data, headers=["NAME", "TYPE", "NULLABLE", "DEFAULT"], tablefmt="plain")],
        ["Primary Key", "\n".join(primary_key)],
        ["Foreign Keys", "\n".join(foreign_keys)],
        ["Constraints", "\n".join(constraints)],
    ]

    # Print in tabular format
    tabular_data = tabulate(data, tablefmt="fancy_grid")
    print(tabular_data)
    if copy_to_clipboard:
        import pyperclip
        pyperclip.copy(tabular_data)
    return

