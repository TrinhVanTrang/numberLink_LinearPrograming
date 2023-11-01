def selectColors(N):
    colors = []
    for i in range(N):
        wavelength = (
            380 + i * (700 - 380) / N
        )  # Tính toán bước sóng (từ 380 đến 750 nanometers)

        # Chuyển đổi bước sóng thành màu RGB
        if 380 <= wavelength < 440:
            r = -(wavelength - 440) / (440 - 380)
            g = 0.0
            b = 1.0
        elif 440 <= wavelength < 490:
            r = 0.0
            g = (wavelength - 440) / (490 - 440)
            b = 1.0
        elif 490 <= wavelength < 510:
            r = 0.0
            g = 1.0
            b = -(wavelength - 510) / (510 - 490)
        elif 510 <= wavelength < 580:
            r = (wavelength - 510) / (580 - 510)
            g = 1.0
            b = 0.0
        elif 580 <= wavelength < 645:
            r = 1.0
            g = -(wavelength - 645) / (645 - 580)
            b = 0.0
        else:
            r = 1.0
            g = 0.0
            b = (wavelength - 645) / (700 - 645)

        # Chuyển đổi thành giá trị RGB trong khoảng [0, 255]
        color = (int(r * 255), int(g * 255), int(b * 255))
        colors.append(color)
    return colors
