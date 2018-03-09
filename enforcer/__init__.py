# -*- coding: utf-8 -*-

import types
import typing
import ast
import inspect


class TypeViolationError(TypeError):
    def __init__(self, variable_name, expected_type, actual_type):
        super().__init__()
        self.variable_name = variable_name
        self.expected_type = expected_type
        self.actual_type = actual_type

    def __repr__(self):
        return '<{}({}, {}, {})>'.format(
            self.__class__.__name__,
            self.variable_name,
            self.expected_type.__name__,
            self.actual_type.__name__,
        )

    def __str__(self):
        return 'Expected {} to have type {}, got type {}'.format(
            self.variable_name,
            self.expected_type.__name__,
            self.actual_type.__name__,
        )


def load(name):
    return ast.Name(id=name, ctx=ast.Load())


def isinstance_ast(name, type_):
    return ast.Call(
        func=load('isinstance'),
        args=[load(name), load(type_)],
        keywords=[],
    )


def type_ast(variable_name):
    return ast.Call(
        func=load('type'),
        args=[load(variable_name)],
        keywords=[],
    )


def raise_type_violation_error_ast(variable_name, expected_type):
    return ast.Raise(
        exc=ast.Call(
            func=load('TypeViolationError'),
            args=[
                ast.Str(s=variable_name),
                load(expected_type),
                type_ast(variable_name),
            ],
            keywords=[],
        ),
        cause=None,
    )


def not_ast(node):
    return ast.UnaryOp(op=ast.Not(), operand=node)


class TypeCheckingVisitor(ast.NodeTransformer):
    def visit_AnnAssign(self, node):
        name = node.target.id
        type_ = node.annotation.id
        return [
            node,
            ast.If(
                test=not_ast(isinstance_ast(name, type_)),
                body=[raise_type_violation_error_ast(name, type_)],
                orelse=[],
            )
        ]


def transform(visitor):
    def deco(function):
        source = ''.join(inspect.getsourcelines(function)[0])
        module = ast.parse(source)
        func = module.body[0]
        visitor.visit(func)
        ast.fix_missing_locations(func)
        module_code = compile(module, '<string>', 'exec')
        globs = function.__globals__.copy()
        globs['TypeViolationError'] = TypeViolationError
        return types.FunctionType(
            module_code.co_consts[0],
            globs,
            function.__name__,
        )
    return deco


enforce = transform(TypeCheckingVisitor())
