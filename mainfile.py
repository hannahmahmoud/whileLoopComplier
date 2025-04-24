from   lexicalAnalysis import lexer_from_file
from ContextFreeGrammer import parse_tokens_to_ast, save_ast_to_file
from semanticAnalyser import SemanticAnalyzer
import json

# 📥 Read input code from external file
with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\Code.txt", "r", encoding="utf-8") as f:
    code = f.read()

# 🔹 Tokenization
tokens = lexer_from_file("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\Code.txt")
with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\Tokens.txt", "w", encoding="utf-8") as f:
    for token in tokens:
        f.write(f"{token}\n")

print(" Tokens saved to token.txt")

# 🌳 Parsing
ast = parse_tokens_to_ast(tokens)
save_ast_to_file(ast)  # This is your existing AST saving logic (likely as ast.json)

with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\AST.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(ast, indent=2))

print(" AST saved to AST.txt")

# ✅ Semantic Analysis
analyzer = SemanticAnalyzer()
symbol_table, errors = analyzer.analyze(ast)

with open("C:\\Users\\User\\Desktop\\AASTMT\\Year 3\\Semester 2\\Projects\\Compliers\\SymbolTable.txt", "w", encoding="utf-8") as f:
    f.write("📘 Symbol Table:\n")
    f.write(json.dumps(symbol_table, indent=2))
    f.write("\n\n")

    if errors:
        f.write(" Semantic Errors:\n")
        for error in errors:
            f.write(f"{error}\n")
    else:
        f.write(" No semantic errors found.\n")

print(" Semantic results saved to semantics.txt")
