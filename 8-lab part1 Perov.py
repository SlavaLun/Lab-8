from PIL import Image

image_path = r"C:\Users\Lunatik\Desktop\Variant-8.jpg"  # Замените <номер варианта> на фактический номер варианта
image = Image.open(image_path)
width, height = image.size

left = (width - 400) // 2
top = (height - 400) // 2
right = left + 400
bottom = top + 400

cropped_image = image.crop((left, top, right, bottom))

cropped_image_path = r"C:\Users\Lunatik\Desktop\Новая папка\cropped_image.jpg"

cropped_image.save(cropped_image_path)

print("Обрезанное изображение сохранено как", cropped_image_path)
