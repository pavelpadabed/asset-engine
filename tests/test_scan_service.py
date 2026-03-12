from application.services.scan_service import ScanService

def test_scan_service(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    service = ScanService()
    results = list(service.scan(tmp_path))
    assert len(results) == 1
    assert results[0].path == file
    assert results[0].size == 5