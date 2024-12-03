#ifndef IR_GENERATOR_H
#define IR_GENERATOR_H

#include "IRNode.h"
#include "IREdge.h"

#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>

namespace ir {

class IRGeneratorVisitor : public clang::RecursiveASTVisitor<IRGeneratorVisitor> {
public:
    explicit IRGeneratorVisitor(clang::ASTContext& context);
    bool VisitFunctionDecl(clang::FunctionDecl* funcDecl);
    // Additional Visit methods for other AST nodes

private:
    clang::ASTContext& context_;
    // Members to store or build the IR
};

class IRGeneratorASTConsumer : public clang::ASTConsumer {
public:
    explicit IRGeneratorASTConsumer(clang::ASTContext& context);
    void HandleTranslationUnit(clang::ASTContext& context) override;

private:
    IRGeneratorVisitor visitor_;
};

} // namespace ir

#endif // IR_GENERATOR_H
