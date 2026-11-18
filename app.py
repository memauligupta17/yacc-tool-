import streamlit as st
import subprocess
import tempfile
from pathlib import Path

st.set_page_config(page_title="Mini YACC Tool", page_icon="⚙️", layout="centered")

st.title("⚙️ Mini YACC Tool using C++")
st.write("Enter an arithmetic expression. The app uses **Flex + Bison (YACC)** to tokenize, parse, and evaluate it.")

st.info("Supported: +, -, *, /, ^, parentheses, decimal numbers, and unary minus.")

expression = st.text_input("Enter expression", value="(10 + 5) * 2 - 8 / 4")
run = st.button("Analyze & Evaluate", type="primary")

BASE_DIR = Path(__file__).parent

def run_parser(expr: str):
    required = ["bison", "flex", "g++"]
    for command in required:
        if subprocess.run(["bash", "-lc", f"command -v {command}"], capture_output=True).returncode != 0:
            return None, f"Required tool not found: {command}. Check packages.txt and redeploy."

    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp)
        for filename in ("parser.y", "lexer.l"):
            (work / filename).write_text((BASE_DIR / filename).read_text(encoding="utf-8"), encoding="utf-8")

        commands = [
            ["bison", "-d", "parser.y"],
            ["flex", "lexer.l"],
            ["g++", "-std=c++17", "parser.tab.c", "lex.yy.c", "-o", "yacc_tool", "-lfl"],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=work, text=True, capture_output=True)
            if result.returncode != 0:
                return None, result.stderr or result.stdout or "Build failed."

        result = subprocess.run(
            [str(work / "yacc_tool")],
            input=expr + "\n",
            cwd=work,
            text=True,
            capture_output=True,
            timeout=10,
        )
        return result.stdout, result.stderr

if run:
    if not expression.strip():
        st.warning("Please enter an expression first.")
    else:
        with st.spinner("Running Flex, Bison and the C++ compiler..."):
            output, error = run_parser(expression)

        if output is None:
            st.error("Could not build the parser.")
            st.code(error)
        else:
            if "Syntax error" in output or "Division by zero" in output or "Invalid expression" in output:
                st.error("The expression could not be evaluated.")
            else:
                st.success("Parsing completed.")
            st.subheader("Parser output")
            st.code(output.strip() or "No output")
            if error.strip():
                with st.expander("Compiler / runtime messages"):
                    st.code(error)

with st.expander("How this project works"):
    st.markdown("""
    1. **Flex (`lexer.l`)** reads the input and identifies numbers and operators.
    2. **Bison/YACC (`parser.y`)** checks whether the token sequence follows the grammar.
    3. Semantic actions calculate the expression value.
    4. The Streamlit interface displays the parser output.
    """)
