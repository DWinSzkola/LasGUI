# Logic.py
import os
import shutil
import laspy


def process_file(input_path: str, output_path: str, settings: dict):
    """
    Główna funkcja backendu.
    Przetwarza plik LAS / CSV / TXT i zapisuje wynik pod output_path.
    Zwraca (success, message).
    """

    if not os.path.exists(input_path):
        return False, "Input file does not exist."

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        return False, "Output folder does not exist."

    output_ext = settings.get("output_format", ".las")
    points_to_render = settings.get("points_to_render", 10.0)

    # Zamiana rozszerzenia wg ustawień
    base, _ = os.path.splitext(output_path)
    output_path = base + output_ext

    try:
        if input_path.lower().endswith(".las"):
            return _process_las_file(input_path, output_path, points_to_render)
        else:
            # Dla innych plików – po prostu kopiujemy
            shutil.copy2(input_path, output_path)
            return True, f"File copied successfully → {output_path}"

    except Exception as e:
        return False, f"Processing error: {str(e)}"


def _process_las_file(input_path: str, output_path: str, points_to_render: float):
    """
    Przetwarzanie LAS przy pomocy laspy.
    Możesz tutaj wkleić swoją logikę filtrowania, klasyfikacji, itd.
    """

    try:
        las = laspy.read(input_path)

        # -----------------------------------------------
        # 👉 PRZYKŁADOWE PRZETWARZANIE
        # (zmień to na własny algorytm)
        # -----------------------------------------------

        # Przykładowy filtr wysokości
        min_z = las.z.min()
        max_z = las.z.max()
        threshold = min_z + (max_z - min_z) * (points_to_render / 100.0)

        mask = las.z >= threshold
        filtered_points = las.points[mask]

        new_las = laspy.create(point_format=las.header.point_format)
        new_las.points = filtered_points

        new_las.header.offsets = las.header.offsets
        new_las.header.scales = las.header.scales

        new_las.write(output_path)

        return True, f"LAS processed successfully → {output_path}"

    except Exception as e:
        return False, f"LAS processing error: {str(e)}"


def move_to_downloads(file_path):
    """Przenosi plik do folderu ~/Downloads"""

    if not os.path.exists(file_path):
        return False, "File does not exist."

    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)

    file_name = os.path.basename(file_path)
    target_path = os.path.join(downloads_dir, file_name)

    try:
        shutil.move(file_path, target_path)
        return True, f"File moved to Downloads → {target_path}"
    except Exception as e:
        return False, str(e)
