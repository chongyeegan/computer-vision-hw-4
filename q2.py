import numpy as np

WORLD_FILE = 'Files/world.txt'
IMG_FILE = 'Files/image.txt'


def concat_one(l):
    l.append(1.0)
    return l


def parse_files(world_file, img_file, world_accum=[], image_accum=[]):
    # read the coordinates of world points
    f = open(world_file, 'r')
    world_x = f.readline().split()
    world_y = f.readline().split()
    world_z = f.readline().split()
    for i in xrange(len(world_x)):
        p = concat_one([float(world_x[i]), float(world_y[i]), float(world_z[i])])
        world_accum.append(p)
    f.close()

    # read the coordinates of image points
    f2 = open(img_file, 'r')
    image_x = f2.readline().split()
    image_y = f2.readline().split()
    for j in xrange(len(image_x)):
        q = concat_one([float(image_x[j]), float(image_y[j])])
        image_accum.append(q)
    f2.close()
    return world_accum, image_accum


if __name__ == '__main__':
    world_accum, image_accum = parse_files(WORLD_FILE, IMG_FILE)

    print world_accum
    print image_accum

    # build A using instructions
    A = []
    for i in xrange(len(world_accum)):
        row1 = [0.0, 0.0, 0.0, 0.0] + [-image_accum[i][2]*x for x in world_accum[i]] + [image_accum[i][1]*x for x in world_accum[i]]
        A.append(row1)
        row2 = [image_accum[i][2]*x for x in world_accum[i]] + [0.0, 0.0, 0.0, 0.0] + [-image_accum[i][0]*x for x in world_accum[i]]
        A.append(row2)

    # the right eigenvector corresponding to the smallest singular value of A
    U, s, V = np.linalg.svd(A, full_matrices=True)  # values in s are sorted in descending order
    # solve for p
    p = V[np.argmin(s), :]
    camera = p.reshape(3, 4)
    print "Projection matrix: ", camera
    for i in xrange(len(image_accum)):
        x = np.array(world_accum[i])
        x_img = np.dot(camera, x)
        print "Reprojection diff Image", [x_img[0]/x_img[2], x_img[1]/x_img[2]] - np.array(image_accum[i][:2])

    # compute the projection center of the camera C
    Up, sp, Vp = np.linalg.svd(camera, full_matrices=True)
    cind = np.argmin(sp)
    c = Vp[cind, :]
    cw = (c/c[3])[0:3]
    print "Projection center:", cw
