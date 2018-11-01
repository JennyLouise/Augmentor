import Augmentor
p = Augmentor.Pipeline("/scratch/jw22g14/HopkinsonFloridaKeys/images/")
p.ground_truth("/scratch/jw22g14/HopkinsonFloridaKeys/masks/")
p.rotate_random_90(probability=0.75)
p.flip_left_right(probability=0.5)
p.flip_top_bottom(probability=0.5)
p.skew(probability=0.2, magnitude=1)
p.crop_by_size(probability=1, width=512, height=512, centre=False)
p.random_distortion(probability=1, grid_width=16, grid_height=16, magnitude=2)
p.sample(3000)
