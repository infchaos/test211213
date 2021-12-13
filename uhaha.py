# -*- coding: utf-8 -*-
import json
from flask import Flask, request, jsonify, make_response
import traceback

global global_ctx
global_ctx={}
method_dict={}

def f(args):
    print(args)
    return args
method_dict['test1']=f
def f(args):
    return [456]+args
method_dict['test2']=f
def f(args):
    exec(args)
    return True
method_dict['exec']=f
def f(args):
    return eval(args)
method_dict['eval']=f
def f(args):
    scope = {'global_ctx':global_ctx}
    exec(args,scope)
    return scope.get('ret',None)
method_dict['exec2']=f
def f(args,data):
    scope = {'global_ctx':global_ctx,'data':data}
    exec(args,scope)
    return scope.get('ret',None)
method_dict['exec3']=f

def handle(params):
    try:
        if 'data' in params:
            return method_dict[params['id']](params['args'],params['data'])
        return method_dict[params['id']](params['args'])
    except Exception:
        traceback.print_exc()
        return None


del f