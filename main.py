from lexicalAnalysis import lexer_from_file, lexer_without_declarations
from parser import parse_tokens_to_ast, save_ast_to_file
from semanticAnalyser import SemanticAnalyzer
from TACGenerator import TACGenerator
from optimizedTAC import TACOptimizer
import json

def main():
    # Read input code
    try:
        with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\Code.txt", "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        exit(1)

    # Tokenization
    try:
        tokens = lexer_from_file("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\Code.txt")
        with open("Tokens.txt", "w", encoding="utf-8") as f:
            for token in tokens:
                f.write(f"{token}\n")
        print("Tokens saved to Tokens.txt")
    except Exception as e:
        print(f"Tokenization error: {str(e)}")
        exit(1)

    # Parsing and AST Generation
    ast = None
    try:
        ast = parse_tokens_to_ast(tokens)
    except SyntaxError as e:
        print(f"Syntax error detected: {str(e)}")
        print("AST generation and saving skipped due to syntax errors.")
        exit(1)

    # Save AST
    try:
        save_ast_to_file(ast)
        with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\AnotatedAST.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(ast, indent=2))
        print("AST saved to AnotatedAST.txt")
    except Exception as e:
        print(f"Error saving AST: {str(e)}")
        exit(1)

    # Semantic Analysis
    try:
        analyzer = SemanticAnalyzer()
        symbol_table, errors = analyzer.analyze(ast)
        with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\symbolTable.txt", "w", encoding="utf-8") as f:
            f.write("Symbol Table:\n")
            f.write(json.dumps(symbol_table, indent=2))
            f.write("\n\n")
            if errors:
                f.write("Semantic Errors:\n")
                for error in errors:
                    f.write(f"{error}\n")
            else:
                f.write("No semantic errors found.\n")
        print("Semantic results saved to symbolTable.txt")
    except Exception as e:
        print(f"Semantic analysis error: {str(e)}")
        exit(1)

    # TAC Generation
    if errors:
        print("Semantic errors detected! TAC generation skipped.")
    else:
        try:
            tac_generator = TACGenerator()
            tac_code = tac_generator.generate_tac(ast)
            with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\TAC.txt", "w", encoding="utf-8") as f:
                for line in tac_code:
                    f.write(line + "\n")
            print("TAC generated and saved to TAC.txt")

            # Optimize TAC
            optimizer = TACOptimizer(
                "C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\TAC.txt",
                "C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\optimized_TAC.txt"
            )
            optimizer.optimize_tac()
            print("Optimized TAC saved to optimized_TAC.txt")

        except Exception as e:
            print(f"Error generating TAC: {str(e)}")
            exit(1)

if __name__ == "__main__":
    main()