# pip install onnx
import onnx
import json
import ast

def parse_names(v):
    """Chuyển chuỗi names trong metadata thành list tên class."""
    v = v.strip()
    try:  # JSON
        obj = json.loads(v)
        if isinstance(obj, dict):
            return [obj[str(i)] for i in range(len(obj))]
        if isinstance(obj, list):
            return obj
    except:
        pass
    try:  # Python dict string
        obj = ast.literal_eval(v)
        if isinstance(obj, dict):
            return [obj[i] for i in range(len(obj))]
        if isinstance(obj, list):
            return obj
    except:
        pass
    return None

def get_input_and_classes(onnx_path):
    model = onnx.load(onnx_path)

    # Lấy thông tin input
    inputs = []
    for vi in model.graph.input:
        dims = [d.dim_value if d.HasField("dim_value") else d.dim_param
                for d in vi.type.tensor_type.shape.dim]
        inputs.append({"name": vi.name, "shape": dims})

    # Lấy tên class từ metadata
    meta = {p.key: p.value for p in model.metadata_props}
    names = None
    for key in ["names", "labels", "classes", "class_names"]:
        if key in meta:
            names = parse_names(meta[key])
            break

    # Nếu không có names → suy ra số lớp
    num_classes = None
    if names:
        num_classes = len(names)
    else:
        for vi in model.graph.output:
            dims = [d.dim_value for d in vi.type.tensor_type.shape.dim]
            if dims and dims[-1] >= 6:
                num_classes = dims[-1] - 5
                break

    return {
        "inputs": inputs,
        "class_names": names,
        "num_classes": num_classes
    }

if __name__ == "__main__":
    onnx_path = "/home/heheboiz/data/PlantGuard/edge/model/resnet50_finetuned_plant_disease.onnx"  # đổi thành đường dẫn file
    info = get_input_and_classes(onnx_path)
    print("Thông tin đầu vào:")
    for inp in info["inputs"]:
        print(f"  - {inp['name']}: shape={inp['shape']}")
    print("\nClass:")
    if info["class_names"]:
        for i, name in enumerate(info["class_names"]):
            print(f"  {i}: {name}")
    else:
        print(f"Không tìm thấy tên class, số lớp ước lượng: {info['num_classes']}")
