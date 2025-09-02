from pyzeebe import ZeebeClient, create_insecure_channel
# para Camunda 8 self-managed. Se usar Camunda Cloud, troque por create_camunda_cloud_channel

def get_zeebe_client():
    # ajuste o host:porta para seu ambiente
    channel = create_insecure_channel("zeebe:26500")
    return ZeebeClient(channel)

def start_gm_create_simple(vars: dict):
    """
    Inicia o processo gm_create_simple no Camunda Zeebe.
    Espera um dicionário com variáveis:
      - cr_id
      - material_number
      - material_type
      - industry_sector
      - material_group
      - base_unit_of_measure
      - language
      - description
    """
    client = get_zeebe_client()
    client.run_process(
        bpmn_process_id="gm_create_simple",  # deve bater com o ID do seu BPMN
        variables=vars
    )
