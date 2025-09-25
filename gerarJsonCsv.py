"""
Este código gera os parametros de coletas, fase e TC do ultronline.
"""
import json
import os
import pandas as pd
import mysql.connector # pip install mysql-connector-python

def generate_json_csv(planta):
    pass

    mydb = mysql.connector.connect(
        host="ultronline.cibxpi1gohmx.us-east-1.rds.amazonaws.com",
        user="2neuron_leitura",
        password="2neuron_leitura",
        database='projeto_ultron_teste'
    )

    modulos_data = pd.read_sql(f"\
    SELECT * FROM Modulos  where Gateways_Plantas_idPlanta='{planta}'", mydb)
    ativos_data = pd.read_sql(f"\
    SELECT * FROM Ativos  where Modulos_Gateways_Plantas_idPlanta='{planta}'", mydb)

    modulos_data.set_index('idModulo', inplace=True)
    ativos_data.set_index('Modulos_idModulo', inplace=True)

    total_df = modulos_data.join(ativos_data[[
        "acionamento", "frequencia_nominal", "tensao_nominal", "corrente_nominal"]])
    print(total_df)


    output = {}
    for id_modulo, row in total_df.iterrows():
        output[id_modulo] = {
            "corrente_l1": row['corrente_l1'],
            "corrente_l2": row['corrente_l2'],
            "corrente_l3": row['corrente_l3'],
            "tensao_l1": row['tensao_l1'],
            "tensao_l2": row['tensao_l2'],
            "tensao_l3": row['tensao_l3'],
            "sentido_tc1": row['sentido_tc1'],
            "sentido_tc2": row['sentido_tc2'],
            "sentido_tc3": row['sentido_tc3'],
            "tc_ratio": row['TC_ratio'],
            "tp_ratio": row['TP_ratio'],
            "tensao_nominal": row['tensao_nominal'],
            "corrente_nominal": row['corrente_nominal'],
            "frequencia_nominal": row['frequencia_nominal'],
            "acionamento": row['acionamento']
        }

    output["padrao"] = {
            "corrente_l1": 0,
            "corrente_l2": 1,
            "corrente_l3": 2,
            "tensao_l1": 5,
            "tensao_l2": 4,
            "tensao_l3": 3,
            "sentido_tc1": 1,
            "sentido_tc2": 1,
            "sentido_tc3": 1,
            "tc_ratio": 5000,
            "tp_ratio": 1,
            "tensao_nominal": 380,
            "corrente_nominal": 100,
            "frequencia_nominal": 60,
            "acionamento": "partida direta",
        }

    with open(f'parametros_ultronline_{planta}.json', 'w') as f:
        json.dump(output, f, indent=4)
        
    mydb.close()


# merged_df = pd.merge(modulos_data, ativos_data, on='key', how='inner')

# configuration_data = pd.DataFrame(
#     data={
#         "id_modulo": modulos_data['idModulo'],
#         "corrente_l1": modulos_data['corrente_l1'],
#         "corrente_l2": modulos_data['corrente_l2'],
#         "corrente_l3": modulos_data['corrente_l3'],
#         "tensao_l1": modulos_data['tensao_l1'],
#         "tensao_l2": modulos_data['tensao_l2'],
#         "tensao_l3": modulos_data['tensao_l3'],
#         "tc_ratio": modulos_data['TC_ratio'],
#         "tp_ratio": modulos_data['TP_ratio']
#     }
# )

# print(configuration_data)