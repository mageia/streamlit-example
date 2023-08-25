import base64

import requests
import streamlit as st

# 设置页面布局为左右分栏
st.set_page_config(layout="wide")


# 向后端OCR服务发送图像并获取识别结果
def ocr_img(image):
    # 假设您的后端OCR服务为http://your-ocr-service，您可以根据实际情况进行修改
    ocr_service_url = "https://ocr.p104.cs.work/ocr/img"

    # 发送POST请求
    response = requests.post(
        ocr_service_url,
        files={"files": ("file", image, "image/png")},
    )

    if response.status_code == 200:
        return response.json().get("result")[0]
    else:
        return "OCR识别失败，请重试。"


def ocr_pdf(pdf):
    # 假设您的后端OCR服务为http://your-ocr-service，您可以根据实际情况进行修改
    ocr_service_url = "https://ocr.p104.cs.work/ocr/pdf"

    # 发送POST请求
    response = requests.post(ocr_service_url, files={"file": ("file", pdf, "application/pdf")})

    if response.status_code == 200:
        return response.json().get("result")[0]
    else:
        return "OCR识别失败，请重试。"


# 主界面
def main():
    st.title("OCR识别应用")

    # 创建左右分栏布局
    col1, col2 = st.columns(2)

    # 左栏（用户上传图片）
    with col1:
        st.subheader("上传图片")
        uploaded_file = st.file_uploader("请选择一张图片", type=["jpg", "jpeg", "png"])

        # 处理上传的文件
        if uploaded_file is not None:
            # 基于文件创建图像数据
            image = uploaded_file.read()
            st.image(image, caption="上传的图片", use_column_width=True)

            # 调用OCR服务进行文字识别
            if st.button("开始识别"):
                ocr_text = ocr_img(image)

                # 在右侧显示文本编辑框
                with col2:
                    st.subheader("文本编辑")
                    edited_text = st.text_area("请编辑识别后的文本", value=ocr_text, height=400)

                    # 保存到后台（数据库）
                    if st.button("保存"):
                        # 这里写保存到数据库的逻辑，您可以根据实际情况进行修改
                        st.success("已保存到数据库！")

        pdf_file = st.file_uploader("请选择PDF文件: ", type="pdf")
        if pdf_file is not None:
            if st.button("开始识别"):
                ocr_text = ocr_pdf(pdf_file)

                # 在右侧显示文本编辑框
                with col2:
                    st.subheader("文本编辑")
                    edited_text = st.text_area("请编辑识别后的文本", value=ocr_text, height=400)

                    # 保存到后台（数据库）
                    if st.button("保存"):
                        # 这里写保存到数据库的逻辑，您可以根据实际情况进行修改
                        st.success("已保存到数据库！")


# 运行主界面
if __name__ == "__main__":
    main()
