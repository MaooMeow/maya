import pymel.core as pm  
# 定义默认相机的名称列表  
default_cameras = ['persp', 'top', 'side', 'front']    
def set_camera_attributes(cameras):  
    for camera in cameras:  
        camShape = camera.getShape()  
        camTransform = camera.getTransform()  
          
        if camShape:  
            cn = camShape.attr('nearClipPlane')  
            cs = camShape.attr('farClipPlane')  
            pm.setAttr(cn, 1)  
            pm.setAttr(cs, 1000000)  
          
        # 假设每个相机都有一个相关的平面节点，这里需要确保这个节点确实存在  
        camPlane = camTransform.name() + 'Plane'  
        if pm.objExists(camPlane):  
            ca = pm.PyNode(camPlane).attr('alphaGain')  
            cd = pm.PyNode(camPlane).attr('depth')  
            pm.setAttr(ca, 0.94)  
            pm.setAttr(cd, 5)  
          
        # 锁定相机的变换属性  
        pm.setAttr(camTransform.tx, lock=True)  
        pm.setAttr(camTransform.ty, lock=True)  
        pm.setAttr(camTransform.tz, lock=True)  
        pm.setAttr(camTransform.rx, lock=True)  
        pm.setAttr(camTransform.ry, lock=True)  
        pm.setAttr(camTransform.rz, lock=True)  
  
def apply_camera_settings(*args):  
    selected_cameras = pm.selected(type='transform')  
    cameras_with_shapes = [cam for cam in selected_cameras if cam.getShape() and cam.getShape().type() == 'camera']  
    set_camera_attributes(cameras_with_shapes)  
        # 过滤掉默认相机  
    filtered_cameras = [cam for cam in selected_cameras if cam.name() not in default_cameras]  
    set_camera_attributes(filtered_cameras)  
  
def create_ui():  
    window = pm.window(title="Camera Attribute Setter")  
    layout = pm.columnLayout()  
     # 列出所有相机并创建复选框以供选择  
    cameras = pm.ls(type='camera')  
    camera_checkboxes = {}  
    for camera in cameras:  
        checkbox = pm.checkBox(label=camera.name(), value=False)  
        camera_checkboxes[camera.name()] = checkbox  
      
    pm.text(label="Select cameras and click the button to apply settings.")  
      
    apply_button = pm.button(label='Apply Camera Settings', command=apply_camera_settings)  
      
    pm.showWindow(window)  
  
create_ui()