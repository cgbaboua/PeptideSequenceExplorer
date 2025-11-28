from functions import *
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Peptide Sequence Explorer",
    page_icon = ":dna:",
    layout="wide"
)

# Définition des list_of_list
list_of_list = []

# Interface Streamlit
st.markdown("<h1 style='text-align: center;color:grey;'>Peptide Sequence Explorer </h1>",unsafe_allow_html=True)
#st.title("Peptide Sequence Explorer")
st.markdown("---")

# Sidebar avec informations
with st.sidebar:
    st.header("Upload your dataset 📥")
    uploaded_file = st.file_uploader("Upload data", type = ["txt","csv","tsv"],label_visibility = "collapsed")
    
    # Initialiser session_state
    if 'is_valid' not in st.session_state:
        st.session_state.is_valid = False
        st.session_state.list_of_list = []

    if uploaded_file is not None:
        valid,message = valider_fichier_sequences(uploaded_file)
        if valid:
            st.session_state.is_valid = True
            uploaded_file.seek(0)
            dataframe = pd.read_table(uploaded_file,header=None)
            for index, row in dataframe.iterrows():
                row = re.findall(r"[A-Za-z0-9]+","".join(row))
                list_of_list.append(row)
            st.session_state.list_of_list = list_of_list
        else:
            st.error(message)
            st.session_state.is_valid = False
            st.session_state.list_of_list = []
    else:
        st.session_state.is_valid = False
        st.session_state.list_of_list = []

    st.header("ⓘ Data informations")
    total = calcul_total(list_of_list)
    if total == 1 :
        st.subheader("No data informations")
    else :
        st.metric("Total number of sequences", f"{total:,}")
        st.metric("Peptide length",f"{len(list_of_list)} amino acids")
    
    st.markdown("---")
    if len(list_of_list) == 0 :
        st.subheader("No positions to analyse")
    else :
        st.subheader("Positions available")
    
    # Afficher les possibilités par position
    for i, pos in enumerate(list_of_list, 1):  
        with st.expander(f"Position {i} ({len(pos)} options)"):
            st.write(", ".join(pos))

# Onglets principaux
tab1, tab2, tab3, tab4 = st.tabs([
    "🎲 Random Sequences ", 
    "📋 First Sequences", 
    "🔍 Motif-based search",
    "📊 Properties"
])

if total < 1000000 : 
    maxvalue=total
else :
    maxvalue=1000000
if total < 100 :
    value=total
else :
    value=100


# Tab 1: Sequences aléatoires
with tab1:
    st.header("Generation of random sequences")
    if not st.session_state.is_valid:
        st.info("*Please upload a valid file in the sidebar to use this feature*")
    n_random = st.number_input(
        "Number of sequences to generate",
        min_value=1,
        max_value=maxvalue,
        value=value,
        step=10,
        disabled=not st.session_state.is_valid
    )
    
    if st.button("🎲 Generate", key="gen_random",disabled=not st.session_state.is_valid):
        with st.spinner("Generation in progress..."):
            sequences = generer_aleatoires(n_random,list_of_list)
            
            st.success(f"✅ {len(sequences)} sequences generated")
            
            # Affichage en DataFrame
            df = pd.DataFrame({
                'Sequence': sequences
                }, index=range(1, len(sequences) + 1))
            df.index.name = 'N°'
            st.dataframe(df, width='stretch')
            
            # Bouton de téléchargement
            csv = df.to_csv(index=True)
            st.download_button(
                label="📤 Export as CSV",
                data=csv,
                file_name="random_sequences.csv",
                mime="text/csv"
            )

# Tab 2: Premières sequences
with tab2:
    st.header("First sequences (alphabetic order)")
    if not st.session_state.is_valid:
        st.info("*Please upload a valid file in the sidebar to use this feature*")
    n_first = st.number_input(
        "Number of sequences to display",
        min_value=1,
        max_value=maxvalue,
        value=value,
        step=10,
        key="n_first",
        disabled=not st.session_state.is_valid
    )
    
    if st.button("📋 Generate", key="gen_first",disabled=not st.session_state.is_valid):
        with st.spinner("Generation in progress..."):
            sequences = generer_premieres(n_first,list_of_list)
            
            st.success(f"✅ {len(sequences)} sequences generated")
            
             # Affichage en DataFrame
            df = pd.DataFrame({
                'Sequence': sequences
                }, index=range(1, len(sequences) + 1))
            df.index.name = 'N°'
            st.dataframe(df, width='stretch')
            
            csv = df.to_csv(index=True)
            st.download_button(
                label="📥 Export as CSV",
                data=csv,
                file_name=f"first_{n_first}_sequences.csv",
                mime="text/csv"
            )

# Tab 3: Recherche par motif
with tab3:
    st.header("Motif-based search")
    if not st.session_state.is_valid:
        st.info("*Please upload a valid file in the sidebar to use this feature*")
    # Choix du mode de recherche
    search_mode = st.radio(
        "Search mode",
        ["Fix position", "Flexible position"],
        horizontal=True,
        disabled=not st.session_state.is_valid
    )
    if search_mode == "Fix position":
        st.info(f"""
        **Instructions:**
        - Use `'-'` as a wildcard character to represent any amino acid
        - The length must be exactly {len(list_of_list)} characters
        - Example: `A--R---K-------` finds all  sequences starting with A, with R in position 4 and K in the position 8
        """)

        col1, col2 = st.columns([3, 1])
        with col1:
            motif = st.text_input(
                f"Enter your motif ({len(list_of_list)} characters)",
                value="-"*len(list_of_list),
                max_chars=len(list_of_list),
                disabled=not st.session_state.is_valid
            ).upper()
        
        with col2:
            max_results = st.number_input(
                "Max results",
                min_value=1,
                max_value=maxvalue,
                value=value,
                disabled=not st.session_state.is_valid
            )
        
        if st.button("🔍 Search", key="search_motif",disabled=not st.session_state.is_valid):
            if len(motif) != len(list_of_list):
                st.error(f"❌ The motif must contains exactly {len(list_of_list)} characters !")
            else:
                errors = []
                for i, char in enumerate(motif):
                    if char != '-':
                        if char not in [x.upper() for x in list_of_list[i]]:
                            errors.append(f"Position {i+1}: '{char}' is not valid at this position. Options avalaible: {', '.join(list_of_list[i])}")
                if errors:
                    st.error("❌ Invalid motif !")
                    for error in errors:
                        st.warning(error)
                else :  
                    with st.spinner("Search in progress..."):
                        sequences = chercher_motif(motif, max_results,list_of_list)
                        if sequences:
                            st.success(f"✅ {len(sequences)} sequence(s) find")
                            # Construction d’un seul DataFrame avec HTML
                            sequences_colored = [highlight_motif(seq, motif) for seq in sequences]

                            df = pd.DataFrame({'N°':range(1, len(sequences)+1),
                                               'Sequence': sequences_colored})
                            
                            # Affichage avec HTML (motifs en rouge)
                            max_height = 600
                            table_html = df.to_html(escape=False, 
                                                    index=False,
                                                    justify="left").replace('<table', '<table style="margin: 0; width:100%;border-collapse: collapse;"')
                            html_block = f"""
                            <div style="
                                width: 100%;
                                max-height: 600px;
                                heigth : auto;
                                overflow-y: scroll;
                                overflow-x: auto;
                                padding: 0;
                                margin: 0 0 20px 0;
                            ">
                                {table_html}
                            </div>
                            """
                            st.markdown(html_block, unsafe_allow_html=True)

                            # Export CSV : nettoyer le HTML en retirant les balises avant export
                            df_csv = pd.DataFrame({'Sequence': sequences}, 
                                index=range(1, len(sequences) + 1))
                            df_csv.index.name = 'N°'
                            
                            csv = df_csv.to_csv(index=True)
                            st.download_button(
                                label="📥 Export as CSV",
                                data=csv,
                                file_name=f"sequences_motif_{motif}.csv",
                                mime="text/csv"
                            )
                        else:
                            st.warning("⚠️ No sequence found for this motif")
    else:  # Mode regex
        st.info("""
                **Instructions:**
                - Use `*` as a wildcard for any subsequence (variable length)
                - Examples:
                    - `*LS*`: finds all sequences containing "LS" anywhere
                    - `A*R`: starts with A, ends with R
                    - `*GPR*`: contains "GPR" somewhere
                    - `*K*S*`: contains K then S (not necessarily consecutive)
                """)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            pattern = st.text_input(
                "Enter your motif",
                value="*LS*",
                key="pattern_regex",
                disabled=not st.session_state.is_valid
            ).upper()
        
        with col2:
            max_results_regex = st.number_input(
                "Max results",
                min_value=1,
                max_value=maxvalue,
                value=value,
                step=10,
                key="max_regex",
                disabled=not st.session_state.is_valid
            )

        if st.button("🔍 Search", key="search_motif",disabled=not st.session_state.is_valid):
            with st.spinner("Search in progress..."):
                sequences = chercher_regex_motif(pattern, max_results_regex,list_of_list)
                if sequences:
                    st.success(f"✅ {len(sequences)} sequence(s) find")
                    # Construction d’un seul DataFrame avec HTML
                    sequences_colored = [highlight_motif_regex(seq, pattern) for seq in sequences]
                    df = pd.DataFrame({'N°':range(1, len(sequences)+1),
                                       'Sequence': sequences_colored})
                            
                    # Affichage avec HTML (motifs en rouge)
                    max_height = 600
                    table_html = df.to_html(escape=False, 
                                            index=False,
                                            justify="left").replace('<table', '<table style="margin: 0; width:100%;border-collapse: collapse;"')
                    html_block = f"""
                    <div style="
                    width: 100%;
                    max-height: 600px;
                    heigth : auto;
                    overflow-y: scroll;
                    overflow-x: auto;
                    padding: 0;
                    margin: 0 0 20px 0;
                    ">
                    {table_html}
                    </div>
                    """
                    st.markdown(html_block, unsafe_allow_html=True)
                            
                    # Export CSV : nettoyer le HTML en retirant les balises avant export
                    df_csv = pd.DataFrame({'Sequence': sequences}, 
                                          index=range(1, len(sequences) + 1))
                    df_csv.index.name = 'N°'
                    
                    csv = df_csv.to_csv(index=True)
                    st.download_button(
                        label="📥 Export as CSV",
                        data=csv,
                        file_name=f"sequences_motif_{pattern}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No sequence found for this motif")

        
# Tab 4: Analyse de propriétés
with tab4:
    st.header("Analysis of sequence properties")
    if not st.session_state.is_valid:
        st.info("*Please upload a valid file in the sidebar to use this feature*")

    seq_input = st.text_input(
        f"Enter a {len(list_of_list)} amino acids sequence",
        value="",
        max_chars=len(list_of_list),
        disabled=not st.session_state.is_valid
    ).upper()
    
    if seq_input:
        if len(seq_input) != len(list_of_list):
            st.error(f"❌ The sequence must contains exactly {len(list_of_list)} characters")
        else:
            # Vérifier si la sequence est valide
            valid = True
            for i, aa in enumerate(seq_input):
                if aa not in list_of_list[i]:
                    valid = False
                    st.error(f"❌ '{aa}' is not valid in position {i+1}. Options: {', '.join(list_of_list[i])}")
                    break
            
            if valid:
                st.success("✅ Valid sequence!")
                
                # Afficher la sequence avec coloration
                st.subheader("Sequence:")
                st.code(seq_input, language=None)
                
                # Calculer et afficher les propriétés
                props = calculer_proprietes(seq_input)
                
                st.subheader("Sequence properties:")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Hydrophobics amino acids", f"{props['Hydrophobics']}/{len(list_of_list)}")
                
                with col2:
                    st.metric("Charged amino acids", f"{props['Charged']}/{len(list_of_list)}")
                    st.metric("Glycines (G)", props['Glycines'])
                
                with col3:
                    st.metric("Polars amino acid", f"{props['Polars']}/{len(list_of_list)}")
                
                # Visualisation de la composition
                st.subheader("Amino acids composition:")
                aa_counts = {}
                for aa in seq_input:
                    aa_counts[aa] = aa_counts.get(aa, 0) + 1
                
                df_comp = pd.DataFrame({
                    'Amino acid': list(aa_counts.keys()),
                    'Occurrence': list(aa_counts.values())
                }).sort_values('Occurrence', ascending=False)
                
                st.bar_chart(df_comp.set_index('Amino acid'))



# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Peptide Sequence Explorer | Developed for biological and computational analysis</p>
</div>
""", unsafe_allow_html=True)
