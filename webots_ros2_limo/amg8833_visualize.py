import time

import serial
import numpy as np
import matplotlib.pyplot as plt

PORT = '/dev/ttyACM0'
BAUD = 115200
PIXEL_COUNT = 64
IMAGE_SHAPE = (8, 8)


def parse_pixel_frame(line):
    """Return one validated 8x8 temperature frame, or None for partial data."""
    fields = line.strip().split(',')
    if len(fields) != PIXEL_COUNT:
        return None

    try:
        pixels = np.asarray(fields, dtype=np.float32)
    except ValueError:
        return None
    if not np.isfinite(pixels).all():
        return None

    return np.flipud(pixels.reshape(IMAGE_SHAPE))


def main():
    fig, ax = plt.subplots()
    image = ax.imshow(
        np.zeros(IMAGE_SHAPE), cmap='inferno', vmin=20, vmax=40)
    fig.colorbar(image, ax=ax, label='Temperature (°C)')
    ax.set_title(f'AMG8833 Real-time Thermal Camera ({PORT}, {BAUD} baud)')
    waiting_text = ax.text(
        0.5, 0.5, 'Waiting for valid sensor data...',
        color='white', ha='center', va='center', transform=ax.transAxes,
        bbox={'facecolor': 'black', 'alpha': 0.7, 'pad': 6})

    plt.ion()
    plt.show(block=False)

    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            print(f'Listening for AMG88xx data on {PORT} at {BAUD} baud.')
            # Opening an Arduino serial port resets many Uno boards. Discard any
            # startup fragments and only render complete frames received after it.
            ser.reset_input_buffer()
            last_valid_frame = time.monotonic()
            warned_no_frames = False
            received_frame = False
            invalid_lines = 0
            while plt.fignum_exists(fig.number):
                raw_line = ser.readline()
                if not raw_line:
                    if (not warned_no_frames
                            and time.monotonic() - last_valid_frame >= 5):
                        print(
                            'No valid 64-value frame received in 5 seconds. '
                            'Check that the AMG88xx sketch is uploaded and '
                            'running, the sensor is connected, and no other '
                            'program is using the serial port.')
                        warned_no_frames = True
                    plt.pause(0.01)
                    continue

                line = raw_line.decode('utf-8', errors='replace')
                frame = parse_pixel_frame(line)
                if frame is None:
                    invalid_lines += 1
                    if invalid_lines <= 3:
                        print(f'Ignoring non-frame serial input: {line.strip()[:100]!r}')
                    continue

                image.set_data(frame)
                if waiting_text is not None:
                    waiting_text.remove()
                    waiting_text = None
                last_valid_frame = time.monotonic()
                if not received_frame or warned_no_frames:
                    print('Receiving AMG88xx temperature frames.')
                received_frame = True
                warned_no_frames = False
                fig.canvas.draw_idle()
                plt.pause(0.01)
    except serial.SerialException as exc:
        print(f'Could not read AMG8833 serial port {PORT}: {exc}')
    except KeyboardInterrupt:
        pass
    finally:
        plt.close(fig)


if __name__ == '__main__':
    main()