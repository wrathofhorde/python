# src/json_handler.py
import json
from pathlib import Path
from typing import Dict, Any


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    JSON 파일을 읽어 딕셔너리로 반환합니다.
    
    Args:
        file_path (str): 읽을 JSON 파일의 경로
        
    Returns:
        Dict[str, Any]: JSON 파일의 내용을 담은 딕셔너리
        
    Raises:
        FileNotFoundError: 지정된 파일이 존재하지 않을 경우
        json.JSONDecodeError: JSON 형식이 유효하지 않을 경우
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON 파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"JSON 파싱 오류: {e}", e.doc, e.pos)

def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    딕셔너리를 JSON 파일로 저장합니다.
    
    Args:
        file_path (str): 저장할 JSON 파일의 경로
        data (Dict[str, Any]): 저장할 딕셔너리 데이터
        
    Raises:
        IOError: 파일 쓰기 중 오류가 발생한 경우
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"JSON 파일 쓰기 오류: {e}")
