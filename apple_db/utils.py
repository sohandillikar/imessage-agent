def sql_output_to_json(output: list[tuple], columns: list[tuple]) -> list[dict]:
    for i, row in enumerate(output):
        output[i] = {columns[j][0] : row[j] for j in range(len(columns))}
    return output