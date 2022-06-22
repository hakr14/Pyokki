from OpenGL.GL import *
from OpenGL.constant import Constant

def compile_shader(code: str, shader_type: Constant):
    header = "#version 330\n"
    ref = glCreateShader(shader_type)
    glShaderSource(ref, header + code)
    glCompileShader(ref)
    if not glGetShaderiv(ref, GL_COMPILE_STATUS):
        message = glGetShaderInfoLog(ref)
        glDeleteShader(ref)
        raise SyntaxError("Shader Error:\n" + message.decode("utf-8"))
    return ref

def initialize_program(vsCode: str, fgCode: str):
    vsID = compile_shader(vsCode, GL_VERTEX_SHADER)
    fgID = compile_shader(fgCode, GL_FRAGMENT_SHADER)
    programID = glCreateProgram()
    glAttachShader(programID, vsID)
    glAttachShader(programID, fgID)
    glLinkProgram(programID)
    if not glGetProgramiv(programID, GL_LINK_STATUS):
        message = glGetProgramInfoLog(programID)
        glDeleteProgram(programID)
        raise RuntimeError("GL Program Error:\n" + message.decode("utf-8"))
    return programID