import cv2

def calculate_target_position(boxes, weights):
    if len(boxes) == 0 or len(weights) == 0:
        raise ValueError("Arguments must be non zero-length lists!")
    if len(boxes) != len(weights):
        raise ValueError("Arguments' lengths should be the same!")

    target_x = 0
    target_y = 0
    weight_total = 0
    for box, weight in zip(boxes, weights):
        x, y, w, h = box

        weight_total += weight * weight

        target_x += (x + w / 2) * weight * weight
        target_y += (y + h / 2) * weight * weight

    target_x /= weight_total
    target_y /= weight_total

    return int(target_x), int(target_y)


def draw_detection_boxes(frame, boxes, weights):
    for idx, weight in enumerate(weights):
        x, y, w, h = boxes[idx]
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        if weight < 0.13:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        elif weight < 0.3:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (190, 30, 0), 2)
        if weight < 0.7:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 122, 255), 2)
        else:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)