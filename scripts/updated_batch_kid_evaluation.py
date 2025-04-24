import os
import tensorflow as tf
import tensorflow_gan as tfgan
import pandas as pd

# Parameter configuration
MAX_FRAMES = 50
original_base = 'frames/original/animation'
compressed_base = 'frames/compressed'
csv_path = 'kid_scores.csv'

def load_images_from_directory(directory, image_size=(299, 299), max_images=MAX_FRAMES):
    image_paths = sorted([
        os.path.join(directory, fname) for fname in os.listdir(directory)
        if fname.lower().endswith(('.png', '.jpg', '.jpeg'))
    ])[:max_images]

    images = []
    for path in image_paths:
        try:
            img = tf.io.read_file(path)
            img = tf.image.decode_image(img, channels=3)
            img = tf.image.resize(img, image_size)
            img = tf.cast(img, tf.float32) / 255.0
            images.append(img)
        except Exception as e:
            print(f"[Skip] Failed to load image: {path}, error: {e}")
            continue
    return tf.stack(images) if images else None

# Load existing results if available
if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path)
else:
    existing_df = pd.DataFrame(columns=["original", "compressed", "kid_mean", "kid_std"])

# Iterate over original-compressed pairs
for original_name in os.listdir(original_base):
    original_path = os.path.join(original_base, original_name)
    if not os.path.isdir(original_path):
        continue

    try:
        original_images = load_images_from_directory(original_path)
        if original_images is None:
            print(f"[Skip] No valid original images found in {original_name}")
            continue
    except Exception as e:
        print(f"[Error] Failed to load original images from {original_name}: {e}")
        continue

    for compressed_name in os.listdir(compressed_base):
        if not compressed_name.startswith(original_name):
            continue

        if ((existing_df["original"] == original_name) &
            (existing_df["compressed"] == compressed_name)).any():
            print(f"[Skip] Already processed: {original_name} vs {compressed_name}")
            continue

        compressed_path = os.path.join(compressed_base, compressed_name)
        try:
            compressed_images = load_images_from_directory(compressed_path)
            if compressed_images is None:
                print(f"[Skip] No valid compressed images found in {compressed_name}")
                continue

            if original_images.shape[0] != compressed_images.shape[0]:
                print(f"[Skip] Frame count mismatch: {original_name} vs {compressed_name}")
                continue

            kid_values = tfgan.eval.kernel_inception_distance(original_images, compressed_images)
            kid_mean = float(tf.reduce_mean(kid_values).numpy())
            kid_std = float(tf.math.reduce_std(kid_values).numpy())

            new_row = pd.DataFrame([{
                'original': original_name,
                'compressed': compressed_name,
                'kid_mean': max(0.0, kid_mean),
                'kid_std': kid_std
            }])

            existing_df = pd.concat([existing_df, new_row], ignore_index=True)
            existing_df.to_csv(csv_path, index=False)

            print(f"[OK] {original_name} vs {compressed_name}: KID={kid_mean:.6f}, std={kid_std:.6f}")
            del compressed_images  # Free memory
        except Exception as e:
            print(f"[Error] Failed to compute KID for {original_name} vs {compressed_name}: {e}")
