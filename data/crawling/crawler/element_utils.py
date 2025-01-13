def switch_frame(driver, frame_name: str):
    try:
        driver.switch_to.frame(frame_name)
    except Exception as e:
        raise f"프레임을 변경할 수 없습니다: {e}"