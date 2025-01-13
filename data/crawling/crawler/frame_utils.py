from selenium.common.exceptions import NoSuchFrameException


def switch_frame(driver, frame_name: str):
    try:
        if frame_name == "root":
            driver.switch_to.default_content()
        else:
            driver.switch_to.frame(frame_name)
    except NoSuchFrameException as e:
        raise ValueError(f"프레임을 {frame_name}으로 변경할 수 없습니다: {e}")
    except Exception as e:
        raise RuntimeError(f"예상치 못한 오류가 발생하였습니다: {e}")
