# Peptide Sequence Explorer

## Table of Contents
- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
- [Application Features](#application-features)
  - [Random Sequence Generation](#random-sequence-generation)
  - [Alphabetic Sequence Listing](#alphabetic-sequence-listing)
  - [Motif-Based Search](#motif-based-search)
  - [Sequence Properties Analysis](#sequence-properties-analysis)
- [Usage Instructions](#usage-instructions)
  - [Uploading Position Data](#uploading-position-data)
  - [Generating Sequences](#generating-sequences)
  - [Searching with Patterns](#searching-with-patterns)
- [Input File Format](#input-file-format)
  - [Format Requirements](#format-requirements)
  - [Format Example](#format-example)
- [Dependencies](#dependencies)
  - [Python Packages](#python-packages)
  - [Installation](#installation)
- [Run the App](#run-the-app)
- [Additional Resources](#additional-resources)
- [Contact](#contact)

## Overview

The Peptide Sequence Explorer is an interactive web application designed for exploring and analyzing peptide sequences based on positional amino acid constraints. Built with Streamlit, this tool enables researchers and biologists to:

- Generate random peptide sequences from a defined search space
- List sequences in alphabetical order
- Search for sequences using fixed-position or flexible regex patterns
- Analyze sequence properties such as hydrophobicity and charge
- Export results in CSV format for further analysis

The application supports customizable amino acid positions through file upload, allowing users to define their own search spaces for peptide exploration.

## System Requirements

- Python 3.9 or higher
- Compatible with Windows, macOS, and Linux
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation

### Clone the Repository

To obtain the latest version of the application, clone the repository using the following command:

```bash
git clone https://github.com/cgbaboua/PeptideSequenceExplorer.git
cd PSExplorer
```

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Application Features

<details id="random-sequence-generation">
  <summary>Random Sequence Generation</summary>
  
  ### Detailed Description

  **Purpose:**  
  Generates a specified number of unique random peptide sequences from the available amino acid combinations at each position.

  **Inputs:**  
  - Number of sequences to generate (1-1,000,000)
  - Valid position file uploaded in the sidebar

  **Processing:**  
  1. Randomly selects amino acids from available options at each position
  2. Ensures uniqueness by using set-based storage
  3. Sorts results alphabetically for consistency

  **Outputs:**  
  - Interactive table displaying generated sequences
  - CSV export option with sequence numbering
  - Success message indicating number of sequences generated

  **Usage Notes:**  
  - Generation is nearly instantaneous for up to 10,000 sequences
  - For very large requests, generation time scales linearly
  - Duplicate sequences are automatically prevented
</details>

<details id="alphabetic-sequence-listing">
  <summary>Alphabetic Sequence Listing</summary>
  
  ### Detailed Description

  **Purpose:**  
  Displays the first N sequences in alphabetical order from the complete search space.

  **Inputs:**  
  - Number of sequences to display (1-1,000,000)
  - Valid position file uploaded in the sidebar

  **Processing:**  
  1. Uses direct mathematical indexing to compute the nth sequence
  2. Avoids iterating through all sequences for efficiency
  3. Returns sequences in strict alphabetical order

  **Outputs:**  
  - Interactive table with numbered sequences
  - CSV export functionality
  - Confirmation message with count

  **Usage Notes:**  
  - Optimized algorithm allows instant retrieval even for the 1,000,000th sequence
  - Useful for systematic exploration of the sequence space
  - Order is deterministic and reproducible
</details>

<details id="motif-based-search">
  <summary>Motif-Based Search</summary>
  
  ### Detailed Description

  **Purpose:**  
  Searches for sequences matching specific patterns using either fixed-position wildcards or flexible regex patterns.

  **Search Modes:**

  **1. Fixed Position Search:**
  - Uses `-` as wildcard for any amino acid
  - Pattern must be exactly 15 characters (or match position file length)
  - Example: `A--R---K-------` finds sequences starting with A, R at position 4, K at position 8
  
  **2. Flexible Pattern Search:**
  - Uses `*` as wildcard for variable-length subsequences
  - Searches for motifs anywhere in the sequence
  - Examples:
    - `*LS*`: Contains "LS" anywhere
    - `A*R`: Starts with A, ends with R
    - `*GPR*`: Contains "GPR" somewhere

  **Inputs:**  
  - Search pattern (fixed or flexible)
  - Maximum number of results to return
  - Valid position file

  **Processing:**  
  1. Validates pattern syntax and amino acid validity
  2. For fixed patterns: generates only valid combinations
  3. For flexible patterns: uses regex matching with highlighting
  4. Colors matched amino acids in red for easy visualization

  **Outputs:**  
  - Scrollable HTML table with colored matches
  - Pattern-specific error messages for invalid searches
  - CSV export of results
  - Visual highlighting of matched positions

  **Usage Notes:**  
  - Fixed position search is faster and recommended for position-specific queries
  - Results are limited to prevent memory issues with large result sets
</details>

<details id="sequence-properties-analysis">
  <summary>Sequence Properties Analysis</summary>
  
  ### Detailed Description

  **Purpose:**  
  Analyzes biochemical and structural properties of individual peptide sequences.

  **Inputs:**  
  - Single peptide sequence 
  - Valid position file

  **Analysis Metrics:**  
  1. **Hydrophobic Amino Acids:** Count of A, V, I, L, M, F, W, P, C residues
  2. **Charged Amino Acids:** Count of D, E, K, R, H residues
  3. **Polar Amino Acids:** Count of S, T, N, Q, Y, E, D, K, R, H residues
  4. **Special Residues:** Glycines counts
  5. **Composition Bar Chart:** Visual breakdown of all amino acids

  **Processing:**  
  1. Validates sequence against position constraints
  2. Calculates compositional statistics
  3. Generates interactive visualizations
  4. Provides metrics for each property category

  **Outputs:**  
  - Metric cards displaying key properties
  - Interactive bar chart of amino acid composition
  - Validation messages for invalid sequences
  - Position-specific error reporting

  **Usage Notes:**  
  - Useful for quick validation of designed sequences
  - Helps assess sequence characteristics before synthesis
  - Can guide refinement of search patterns based on desired properties
</details>

## Usage Instructions

### Uploading Position Data

1. **Prepare your position file** in tsv, csv or txt format
2. **Upload the file** using the file uploader in the sidebar
3. **Verify validation** - the app will display:
   - ❌ Error messages specifying any formatting issues
   - Total number of possible sequences
   - Available amino acids per position

### Generating Sequences

1. **Navigate** to either "Random Sequences" or "First Sequences" tab
2. **Enter** the desired number of sequences
3. **Click** the Generate button
4. **Review** results in the interactive table
5. **Download** as CSV if needed using the Export button

### Searching with Patterns

**Fixed Position Search:**
1. Select "Fix position" mode
2. Enter pattern using `-` for wildcards (e.g., `A--E---K-------`)
3. Set maximum results
4. Click Search
5. Review highlighted results

**Flexible Pattern Search:**
1. Select "Flexible position" mode
2. Enter pattern using `*` for wildcards (e.g., `*LS*`)
3. Set maximum results
4. Click Search
5. Examine colored matches in results

## Input File Format

### Format Requirements

- **One line per position :**  The number of lines determines the peptide length
- **Separator - Use** : `/`,`-`, `_`, or `space` to separate amino acids
- **Standard amino acid codes** (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y)
- **No duplicate amino acids** in the same position
- **UTF-8 encoding**
- More options = more possibilities: The number of amino acids per line defines how many choices exist at that position

### Format Example
```bash
# 15 aa-length sequence with varying options per position
A/D/G/L/P/R/S    # Position 1: 7 options
K/R              # Position 2: 2 options
G                # Position 3: 1 option (fixed)
...
```
```bash
# Using different separators (all valid)
A-D-G-L
A_G_L_P
A G L P R
A/G/L/P/R/S
```

### Common Errors and Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid amino acid" | Contains non-standard code | Use only standard 20 amino acids |
| "Duplicates detected" | Same AA listed twice in position | Remove duplicate entries |

## Dependencies

### Python Packages
- **streamlit** (1.49.1): Web application framework
- **pandas** (2.3.2): Data manipulation and CSV export
- **re** (built-in): Regular expression pattern matching
- **itertools** (built-in): Efficient sequence generation
- **random** (built-in): Random sequence sampling

### Installation
All dependencies are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## Run the app
Application is directly available on this website : [https://peptideseqexplorer-iric.streamlit.app](https://peptideseqexplorer-iric.streamlit.app)

### Locally
Run the application locally with:
```bash
streamlit run PSExplorer.py
```

### On the web site


## Additional Resources

- **Streamlit Documentation:** https://docs.streamlit.io
- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Python Regex Guide:** https://docs.python.org/3/library/re.html

## Contact

For questions, issues, or contributions, please contact:
- **Developer:** Cassandra Gbaboua
- **Institution:** Université de Montréal
- **GitHub Issues:** [Create an issue](https://github.com/cgbaboua/PeptideSequenceExplorer/issue)

---

**Peptide Sequence Explorer** | Developed for biological and computational analysis
