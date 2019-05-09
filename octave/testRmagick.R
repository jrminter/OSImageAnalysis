library(magick)
cells <- image_read("D:/Data/images/key-test/ropensci/uv1a-bovine.jpg")
cells %>%
    image_channel(channel = "blue") %>%
    image_morphology(method = "OpenIntensity", kernel = "ConvexHull",
                     iterations = 10) %>%
    image_morphology(method = "Dilate", kernel = "Disk") %>%
    image_morphology(method = "Erode", kernel = "Disk") %>%
    image_fuzzycmeans() %>% image_threshold(type = "white") %>%
    image_connect() %>% image_split(keep_color = FALSE) %>%
    image_composite(cells, operator = "Out") %>%
    image_resize('x300') %>% image_animate(fps = 1)
