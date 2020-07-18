Title: The GANdam Project Part 2 : Space Magic
Date: 2019-09-28 20:00
Category: Machine learning
Tags: gundam,gan,dcgan,ai
Cover: https://gazoche.xyz/images/gandam/original_dataset.png
SubTitle: Where a GAN learns kit-bashing

Small update on the GANdam project ! If you don't know what I'm talking about, part 1 is [here](https://gazoche.xyz/the-gandam-project.html). I'll try to keep it shorter this time...

## Improvements

I did some experimentation and here are the changes I came up with :

* I decided to remove the fully connected layers and bump up the number and sizes of convolutional layers instead. Convolutional layers are much cheaper since the training does not have to deal with huge matrices of parameters.

* I raised the dimensionality of the latent space.

* Even without fully connected layers, the two previous changes were too much for my GPU to handle, so I had to halve the batch size.

* In part 1, I explained how the problem of some mechas facing different directions was solved by augmenting the original dataset with a mirrored copy of all of them. I realized this probably confused the network more than it helped it, so I instead went through the dataset and manually corrected the orientations. I also removed all the weird unique mobile suits that weren't "bipedal" enough, again to help the network recenter its focus.


The GAN performs much better now (the generated samples look objectively closer to real mechas), but in retrospect my exploration of the parameters wasn't very scientific. I made a lot of changes simultaneously, and therefore when the performance improved I couldn't be sure which one of them was responsible for it. I think the general increase in the number of parameters helped a lot, and so did the larger latent space, but it's difficult to be sure.

In the future, I'll try to keep the improvements more incremental.


## Mode collapse

At some point I ran into an issue well known in GAN training : mode collapse.

Mode collapse happens when the generator finds a local minimum in the form of a particular output distribution (the "mode") that's very good at fooling the discriminator, and decides the best course of action is to take all of its outputs from that distribution. Every sample starts to look the same, until the discriminator catches on and counters the generator by detecting this particular mode and always rejecting it. But then the generator settles on another local minimum, the discriminator has to catch up again, and the cycle never ends. This is of course a situation we want to avoid, because neither the generator nor the discriminator learn to generalize properly when they are stuck in this little game.

I found out most of my earlier trainings had, in fact, succumbed to this issue. When I tried taking more than one sample out of the final models, it was obvious that the modes had collapsed because all samples looked nearly identical.

![Samples from one of my mode-collapsed generators]({static}/images/gandam-part2/mode_collapsed_samples.png "Samples from one of my mode-collapsed generators")

Why didn't realize it before ? Well, simply because I had never actually sampled the final models before. All the results showcased in Part 1 were obtained by sampling *ONE* image every few epochs, during training. And since the training was still going, the collective, collapsed mode was still shifting around, creating different results over time but the same results at a given moment. In other words, the variance in the sampled images was due to the training, not the network itself.

The final network I came up with doesn't exhibit the mode collapse issue anymore, but again because of my eagerness to try too many changes at once, I am not sure which one made it go away. My intuition is that it may be the higher latent space dimensionality, but that needs further confirmation.

## The results

Here are some images created by the new generator. This time, they are all randomly sampled from the final model, and I didn't bother selecting the best ones.

![Samples from the improved GAN]({static}/images/gandam-part2/best_samples.png "Samples from the improved GAN")

The improvement is pretty obvious, and we can make out some recognizable features without too much squinting or interpretation. For example, second row, first column has the general shape of a [Gelgoog](https://www.mahq.net/mecha/gundam/msgundam/ms-14a.htm) but with a different color scheme. First row, second column looks to be a [Zaku](https://www.mahq.net/mecha/gundam/msgundam/ms-06f.htm) head on top of a sleeker Gundam body (this is particularly funny because [a similar hybrid](https://gundam.fandom.com/wiki/MSZ-006_Zeta_Gundam#Special_Equipment_.26_Features) actually exists within the Gundam universe, but it wasn't part of the training dataset).

## Future improvements

There is still a lot of room for improvement and I believe the GAN has not shown its true potential yet. For now, I think I'll pushing my GPU to its limits and see if bumping the parameters count even more improves the results ; if not it'll be time to start exploring new architectures.