import numpy as np


def create_visual_vocabulary(image_set, patch_dim):
    """
    Funzione per creare il vocabolario delle immagini
    params:
        - image_set : insieme rappresentativo delle immagini da cui estrarre le visual words
        - patch_dim : dimensione delle visual words
    returns:
        - visual_vocab : vocabolario delle visual words
    """

    visual_vocab = []   # inizializzazione del visual vocabulary

    # estrazione delle visual words
    for image in image_set:
        for i in range(image.shape[0] // patch_dim):
            for j in range(image.shape[1] // patch_dim):
                visual_vocab.append(image[i * patch_dim : (i + 1) * patch_dim, j * patch_dim : (j + 1) * patch_dim])
    return visual_vocab

def create_bovw(image, visual_vocab, patch_dim):
    """
    Funzione per creare una BoVW per l'immagine di input
    params:
        - image : immagine di cui creare la BoVW
        - visual_vocab : vocabolario delle visual words
        - patch_dim : dimensione delle visual words
    returns: 
        - image_bovw : BoVW dell'immagine di input
    """
    # estrazione delle visual words dall'immagine di input
    image_vw = []
    for i in range(image.shape[0] // patch_dim):
        for j in range(image.shape[1] // patch_dim):
            image_vw.append(image[i * patch_dim : (i + 1) * patch_dim, j * patch_dim : (j + 1) * patch_dim])
    
    image_bovw = np.zeros((len(visual_vocab), ))   # inizializzazione BoVW
    for vword in image_vw:
        min_dist = float('inf')
        min_index = -1
        for idx, vocab_word in enumerate(visual_vocab):
            # calcolo della visual word del vocabolario che più somiglia alla visual word 
            # dell'immagine che vogliamo codificare
            dist = np.sum((vword - vocab_word) ** 2)
            if dist < min_dist:
                min_dist = dist
                min_index = idx
        image_bovw[min_index] += 1  # aumento del bin della vword corrispondente
    return image_bovw