from OpenGL import GL
from OpenGL.constant import Constant

def compile_shader(code: str, shader_type: Constant):
    header = "#version 130\n#extension GL_ARB_shading_language_420pack: require\n"
    ref = GL.glCreateShader(shader_type)
    GL.glShaderSource(ref, header + code)
    GL.glCompileShader(ref)
    if not GL.glGetShaderiv(ref, GL.GL_COMPILE_STATUS):
        message = GL.glGetShaderInfoLog(ref)
        GL.glDeleteShader(ref)
        raise SyntaxError("Shader Error:\n" + message.decode("utf-8"))
    return ref

def initialize_program(vsCode: str, fgCode: str):
    vsID = compile_shader(vsCode, GL.GL_VERTEX_SHADER)
    fgID = compile_shader(fgCode, GL.GL_FRAGMENT_SHADER)
    programID = GL.glCreateProgram()
    GL.glAttachShader(programID, vsID)
    GL.glAttachShader(programID, fgID)
    GL.glLinkProgram(programID)
    if not GL.glGetProgramiv(programID, GL.GL_LINK_STATUS):
        message = GL.glGetProgramInfoLog(programID)
        GL.glDeleteProgram(programID)
        raise RuntimeError("GL Program Error:\n" + message.decode("utf-8"))
    return programID