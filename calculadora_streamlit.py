import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Custos e Margens - Mercado Livre",
    page_icon="💰",
    layout="wide"
)

# Título e descrição
st.title("Calculadora de Custos e Margens - Mercado Livre")
st.markdown("Calcule custos, taxas, lucros e margens para seu kit de utilidades domésticas no Mercado Livre.")

# Criar abas
tab1, tab2, tab3 = st.tabs(["Calculadora", "Histórico", "Sobre"])

with tab1:
    # Layout em colunas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Dados do Produto")
        
        # Custos dos itens
        st.markdown("### Custos dos Itens")
        # Usando valores padrão dos dados fornecidos anteriormente
        custo_dispenser = st.number_input("Dispenser + rodinho de pia (R$)", min_value=0.0, value=15.85, format="%.2f", key="custo_dispenser")
        custo_lixeira = st.number_input("Lixeira de pia (R$)", min_value=0.0, value=12.15, format="%.2f", key="custo_lixeira")
        custo_escorredor = st.number_input("Escorredor de pratos (R$)", min_value=0.0, value=19.47, format="%.2f", key="custo_escorredor")
        custo_esponja = st.number_input("Esponja mágica (custo unitário R$)", min_value=0.0, value=1.33, format="%.2f", key="custo_esponja")
        qtd_esponjas_kit = st.number_input("Quantidade de esponjas por kit", min_value=1, value=2, step=1, key="qtd_esponjas_kit")
        
        # Quantidades (para cálculo do frete)
        # st.markdown("### Quantidades (para frete)")
        # qtd_dispenser = st.number_input("Quantidade de dispensers comprados", min_value=1, value=24, step=1, key="qtd_dispenser")
        # qtd_lixeira = st.number_input("Quantidade de lixeiras compradas", min_value=1, value=24, step=1, key="qtd_lixeira")
        # qtd_escorredor = st.number_input("Quantidade de escorredores comprados", min_value=1, value=24, step=1, key="qtd_escorredor")
        # qtd_esponja_total = st.number_input("Quantidade total de esponjas compradas", min_value=1, value=200, step=1, key="qtd_esponja_total")
        qtd_kits = st.number_input("Quantidade total de kits a montar (para rateio do frete)", min_value=1, value=24, step=1, key="qtd_kits")
        
        # Outros custos
        st.markdown("### Outros Custos")
        frete_total_compra = st.number_input("Custo total do frete de compra (R$)", min_value=0.0, value=450.0, format="%.2f", key="frete_total_compra")
        icms_perc = st.number_input("Alíquota ICMS (%)", min_value=0.0, max_value=100.0, value=12.0, format="%.2f", key="icms_perc")
        
    with col2:
        st.subheader("Dados de Venda")
        
        # Preço de venda
        preco_venda = st.number_input("Preço de venda do kit (R$)", min_value=0.0, value=129.90, format="%.2f", key="preco_venda") # Ajustado para valor mais realista
        
        # Tipo de anúncio
        tipo_anuncio = st.radio("Tipo de anúncio no Mercado Livre", ["Clássico", "Premium"], key="tipo_anuncio")
        
        # Taxas do Mercado Livre
        st.markdown("### Taxas do Mercado Livre")
        taxa_ml_perc_dict = {"Clássico": 13.0, "Premium": 17.0}
        taxa_ml_perc = taxa_ml_perc_dict[tipo_anuncio]
        st.info(f"Taxa de comissão: {taxa_ml_perc}% do valor de venda")
        
        custo_frete_ml = st.number_input("Custo estimado do frete grátis ML (R$)", min_value=0.0, value=25.00, format="%.2f", key="custo_frete_ml") # Valor médio comum
        
        # Botão de cálculo
        if st.button("Calcular Resultados", type="primary", use_container_width=True, key="calcular"):
            # Cálculo do custo total do kit
            custo_itens = custo_dispenser + custo_lixeira + custo_escorredor + (custo_esponja * qtd_esponjas_kit)
            frete_por_kit = frete_total_compra / qtd_kits if qtd_kits > 0 else 0
            icms_valor = custo_itens * (icms_perc / 100)
            custo_total_kit = custo_itens + frete_por_kit + icms_valor
            
            # Cálculo das taxas do ML
            taxa_ml_valor = preco_venda * (taxa_ml_perc / 100)
            taxas_totais_ml = taxa_ml_valor + custo_frete_ml
            
            # Cálculo do lucro e margem
            lucro_liquido = preco_venda - custo_total_kit - taxas_totais_ml
            margem_liquida = (lucro_liquido / preco_venda) * 100 if preco_venda > 0 else 0
            
            # Exibir resultados
            st.markdown("--- ")
            st.subheader("📊 Resultados do Cálculo")
            
            # Métricas principais
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Custo Total do Kit", f"R$ {custo_total_kit:.2f}")
            col_b.metric("Taxas Totais ML", f"R$ {taxas_totais_ml:.2f}")
            col_c.metric("Lucro Líquido por Kit", f"R$ {lucro_liquido:.2f}", delta=f"{margem_liquida:.1f}% Margem")
            
            # Detalhamento
            with st.expander("Ver Detalhamento dos Custos e Taxas"):
                detalhamento_custo = {
                    "Componente": ["Custo dos Itens", "Frete de Compra (por kit)", "ICMS (sobre itens)"],
                    "Valor (R$)": [f"{custo_itens:.2f}", f"{frete_por_kit:.2f}", f"{icms_valor:.2f}"]
                }
                st.table(pd.DataFrame(detalhamento_custo).set_index("Componente"))
                
                detalhamento_taxa = {
                    "Componente": [f"Comissão ML ({taxa_ml_perc}%) ", "Frete Grátis ML"],
                    "Valor (R$)": [f"{taxa_ml_valor:.2f}", f"{custo_frete_ml:.2f}"]
                }
                st.table(pd.DataFrame(detalhamento_taxa).set_index("Componente"))
            
            # Avaliação de viabilidade
            st.markdown("#### Avaliação de Viabilidade")
            if lucro_liquido <= 0:
                st.error(f"🚨 PREJUÍZO de R$ {-lucro_liquido:.2f} por kit! Este preço de venda não cobre os custos.")
                preco_equilibrio = custo_total_kit + taxas_totais_ml
                st.warning(f"💡 Preço mínimo para cobrir custos (ponto de equilíbrio): R$ {preco_equilibrio:.2f}")
            elif margem_liquida < 10:
                st.warning(f"⚠️ ATENÇÃO: Margem de lucro baixa ({margem_liquida:.1f}%). Considere revisar custos ou preço.")
            else:
                st.success(f"✅ LUCRO: Margem de {margem_liquida:.1f}% parece viável.")
            
            # Gráfico de composição do preço
            st.markdown("#### Composição do Preço de Venda")
            fig, ax = plt.subplots()
            componentes = [f'Custo Kit\nR${custo_total_kit:.2f}', f'Taxas ML\nR${taxas_totais_ml:.2f}', f'Lucro\nR${lucro_liquido:.2f}']
            valores = [custo_total_kit, taxas_totais_ml, max(0, lucro_liquido)] # Evita lucro negativo no gráfico
            cores = ['#ff6961', '#ffb480', '#90ee90' if lucro_liquido > 0 else '#d3d3d3'] # Vermelho, Laranja, Verde/Cinza
            
            wedges, texts, autotexts = ax.pie(valores, labels=None, autopct='%1.1f%%', startangle=90, colors=cores, pctdistance=0.85)
            ax.legend(wedges, componentes, title="Componentes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.setp(autotexts, size=8, weight="bold", color="white")
            ax.set_title("Distribuição do Preço de Venda")
            st.pyplot(fig)
            
            # Salvar no histórico (usando session_state)
            if 'historico' not in st.session_state:
                st.session_state.historico = []
                
            # Limitar histórico para evitar uso excessivo de memória
            MAX_HISTORICO = 50
            if len(st.session_state.historico) >= MAX_HISTORICO:
                st.session_state.historico.pop(0) # Remove o mais antigo
                
            st.session_state.historico.append({
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Preço Venda (R$)': preco_venda,
                'Custo Kit (R$)': custo_total_kit,
                'Taxas ML (R$)': taxas_totais_ml,
                'Lucro (R$)': lucro_liquido,
                'Margem (%)': margem_liquida,
                'Tipo Anúncio': tipo_anuncio
            })
            st.toast("Cálculo salvo no histórico!")

with tab2:
    st.subheader("📜 Histórico de Cálculos")
    
    if 'historico' in st.session_state and st.session_state.historico:
        # Exibir em ordem decrescente (mais recente primeiro)
        df_historico = pd.DataFrame(st.session_state.historico[::-1]) 
        # Formatando colunas numéricas
        format_dict = {
            'Preço Venda (R$)': '{:.2f}',
            'Custo Kit (R$)': '{:.2f}',
            'Taxas ML (R$)': '{:.2f}',
            'Lucro (R$)': '{:.2f}',
            'Margem (%)': '{:.1f}%'
        }
        st.dataframe(df_historico.style.format(format_dict), use_container_width=True)
        
        # Botão para limpar histórico
        if st.button("Limpar Histórico", key="limpar_hist"):
            st.session_state.historico = []
            st.experimental_rerun()
    else:
        st.info("Nenhum cálculo realizado ainda. Use a aba Calculadora para gerar resultados.")

with tab3:
    st.subheader("ℹ️ Sobre esta Calculadora")
    st.markdown("""
    Esta aplicação web foi desenvolvida para auxiliar no cálculo de custos, taxas, lucros e margens para kits de produtos vendidos no Mercado Livre.
    
    **Funcionalidades:**
    - Entrada de custos detalhados dos itens e frete.
    - Cálculo automático do custo total do kit, incluindo ICMS e frete rateado.
    - Estimativa das taxas do Mercado Livre (comissão + frete grátis).
    - Cálculo do lucro líquido e margem percentual.
    - Visualização gráfica da composição do preço.
    - Histórico dos cálculos realizados durante a sessão.
    
    **Como usar:**
    1. Preencha os custos dos itens, quantidades e outros custos na aba "Calculadora".
    2. Informe o preço de venda desejado e o tipo de anúncio.
    3. Ajuste o custo estimado do frete grátis do ML, se necessário.
    4. Clique em "Calcular Resultados".
    5. Analise os resultados, gráficos e a avaliação de viabilidade.
    6. Consulte cálculos anteriores na aba "Histórico".
    
    **Observações:**
    - Os valores de taxas de comissão do Mercado Livre são baseados nas políticas de Abril/2025 (13% Clássico, 17% Premium). Verifique sempre os valores atuais na plataforma.
    - O custo do frete grátis do ML é uma estimativa e pode variar.
    - O histórico é armazenado apenas durante a sessão atual do navegador.
    """)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Streamlit | 2025")

