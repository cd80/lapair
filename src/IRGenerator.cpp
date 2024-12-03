#include "IRGenerator.h"

using namespace ir;
using namespace clang;

// Implementation of IRGeneratorVisitor

IRGeneratorVisitor::IRGeneratorVisitor(ASTContext& context)
    : context_(context) {
    // Initialize any necessary members
}

bool IRGeneratorVisitor::VisitFunctionDecl(FunctionDecl* funcDecl) {
    if (funcDecl->hasBody()) {
        // Example: Create a Node for the function
        std::string funcName = funcDecl->getNameInfo().getName().getAsString();
        auto funcNode = std::make_shared<Node>(funcName);
        // Store or process the Node as needed

        // You can traverse further into the function body if needed
    }
    return true; // Return true to continue traversal
}

// Implement additional Visit methods as needed

// Implementation of IRGeneratorASTConsumer

IRGeneratorASTConsumer::IRGeneratorASTConsumer(ASTContext& context)
    : visitor_(context) {
}

void IRGeneratorASTConsumer::HandleTranslationUnit(ASTContext& context) {
    // Start the AST traversal
    visitor_.TraverseDecl(context.getTranslationUnitDecl());
}
