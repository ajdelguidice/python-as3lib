from __future__ import annotations


class Context3D:
    ...


class Context3DBlendFactor:
    ...


class Context3DBufferUsage:
    ...


class Context3DClearMask:
    ...


class Context3DCompareMode:
    ...


class Context3DFillMode:
    ...


class Context3DMipFilter:
    ...


class Context3DProfile:
    ...


class Context3DProgramType:
    ...


class Context3DRenderMode:
    ...


class Context3DStencilAction:
    ...


class Context3DTextureFilter:
    ...


class Context3DTextureFormat:
    ...


class Context3DTriangleFace:
    ...


class Context3DVertexBufferFormat:
    ...


class Context3DWrapModer:
    ...


class IndexBuffer3D:
    ...


class Program3D:
    ...


class textures:
    class CubeTexture:
        ...

    class RectagleTexture:
        ...

    class Texture(textures.TextureBase):
        def __init__(self):
            raise NotImplementedError

        def uploadCompressedTextureFromByteArray(data, byteArrayOffset, async_):
            raise NotImplementedError

        def uploadFromBitmapData(source, miplevel=0):
            raise NotImplementedError

        def uploadFromBitmapDataAsync(source, miplevel=0):
            raise NotImplementedError

        def uploadFromByteArray(data, byteArrayOffset, miplevel=0):
            raise NotImplementedError

        def uploadFromByteArrayAsync(data, byteArrayOffset, miplevel=0):
            raise NotImplementedError

    class TextureBase:
        def __init__(self):
            self.dimensions = [None, None]  # width, height
            self.format_ = None
            self.data = None  # byteArray

        def dispose():
            """
            Frees all GPU resources associated with this texture. After disposal, calling upload() or rendering with this object fails.
            """
            ...

    class VideoTexture:
        ...


class VertexBuffer3D:
    ...
