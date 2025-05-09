from lexicalAnalysis import lexer_from_file, lexer_without_declarations
from parser import parse_tokens_to_ast, save_ast_to_file
from semanticAnalyser import SemanticAnalyzer
from TACGenerator import TACGenerator
from commonSubElmination import commonSubElmination
from codeMovement import read_tac_from_file,loop_invariant_code_motion,save_tac_to_file
from constantFolding import constant_folding,save_tac_to_file_1,read_tac_from_file_1
from constantPropagation import constant_propagation,save_tac_to_file_2,read_tac_from_file_2
from deadCodeElmination import save_tac_to_file_3, read_tac_from_file_3, dead_code_elimination
import json
import os

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
            
            # Sub code elmination
            optimizer = commonSubElmination(
                "C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\TAC.txt",
                "C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\subCommonElminationOutput.txt"
            )
            optimizer.optimize_tac()
            print("subCodeElimination is  generated and saved to subCommonElminationOutput.txt")
            
            # Code Movement
            input_file = os.path.expanduser("subCommonElminationOutput.txt")
            output_file = os.path.expanduser("codeMovementOutput.txt")
            tac = read_tac_from_file(input_file)
            optimized_tac = loop_invariant_code_motion(tac)
            save_tac_to_file(optimized_tac, output_file)
            print(f"\nOptimized TAC saved to: {output_file}")
            
            #constant folding 
            input_fileOfConstantFolding = os.path.expanduser("codeMovementOutput.txt")
            output_fileConstantFolding = os.path.expanduser("constantFoldingOutput.txt")
            tac1 = read_tac_from_file_1(input_fileOfConstantFolding)
            folded_tac = constant_folding(tac1)
            save_tac_to_file_1(folded_tac, output_fileConstantFolding)
            print(f"\nFolded TAC saved to: {output_fileConstantFolding}")
            
            
            # constant propagation 
            input_fileConstantPropagation = os.path.expanduser("constantFoldingOutput.txt")
            output_fileConstantPropagation = os.path.expanduser("constantPropagationOutput.txt")
            tac2 = read_tac_from_file_2(input_fileConstantPropagation)
            optimized_tac = constant_propagation(tac2)
            save_tac_to_file_2(optimized_tac, output_fileConstantPropagation)
            print(f"\nOptimized TAC saved to: {output_fileConstantPropagation}")
            
            
            # dead code elemination 
            input_fileDeadCodeElemination= "constantPropagationOutput.txt"
            output_fileDeadCodeElemination = "TAC_Optimized.txt"
            tac3 = read_tac_from_file_3(input_fileDeadCodeElemination)
            optimized = dead_code_elimination(tac3)
            save_tac_to_file_3(optimized, output_fileDeadCodeElemination)
            print(f"\n✅ Optimized TAC saved to: {output_fileDeadCodeElemination}")
            
            
            
            
            
            
            
        
        except Exception as e:
            print(f"Error generating TAC: {str(e)}")
            exit(1)

if __name__ == "__main__":
    main()