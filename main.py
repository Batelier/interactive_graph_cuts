from src.mask import Mask

print("Interactive Graph Cut for Computer Vision \nBased on Jolly and and Boykov Paper \n"
      "--------------------------------------------------------------------------------")

filename = 'src/img_test/lotus.jpg'

mask = Mask().makeMask(filename)
print(mask)