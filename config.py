# -*- coding: utf-8 -*-
# @Author       : William
# @Project      : TextGAN-william
# @FileName     : config.py
# @Time         : Created at 2019-03-18
# @Blog         : http://zhiweil.ml/
# @Description  :
# Copyrights (C) 2018. All Rights Reserved.
import os
import re
import time
import torch
from time import strftime, localtime

# ===Program===
if_test = False
CUDA = True
if_save = True
data_shuffle = False  # False
oracle_pretrain = True  # True
gen_pretrain = False
dis_pretrain = False
clas_pretrain = False

run_model = 'seqgan'  # seqgan, leakgan, maligan, jsdgan, relgan, sentigan
k_label = 2  # num of labels, >=2
gen_init = 'truncated_normal'  # normal, uniform, truncated_normal
dis_init = 'uniform'  # normal, uniform, truncated_normal

# ===Oracle or Real, type===
if_real_data = False  # if use real data
dataset = 'oracle'  # oracle, image_coco, emnlp_news, amazon_app_book, mr15
model_type = 'vanilla'  # vanilla, RMC (custom)
loss_type = 'rsgan'  # standard, JS, KL, hinge, tv, LS, rsgan (for RelGAN)
vocab_size = 5000  # oracle: 5000, coco: 6613, emnlp: 5255, amazon_app_book: 6418, mr15: 6289
max_seq_len = 20  # oracle: 20, coco: 37, emnlp: 51, amazon_app_book: 40
ADV_train_epoch = 2000  # SeqGAN, LeakGAN-200, RelGAN-3000
extend_vocab_size = 0  # plus test data, only used for Classifier

temp_adpt = 'exp'  # no, lin, exp, log, sigmoid, quad, sqrt
temperature = 1

# ===Basic Train===
samples_num = 10000  # 10000, mr15: 2000,
MLE_train_epoch = 150  # SeqGAN-80, LeakGAN-8, RelGAN-150
PRE_clas_epoch = 10
inter_epoch = 15  # LeakGAN-10
batch_size = 64  # 64
start_letter = 1
padding_idx = 0
start_token = 'BOS'
padding_token = 'EOS'
gen_lr = 0.01  # 0.01
gen_adv_lr = 1e-4  # RelGAN-1e-4
dis_lr = 1e-4  # SeqGAN,LeakGAN-1e-2, RelGAN-1e-4
clas_lr = 1e-3
clip_norm = 5.0

pre_log_step = 10
adv_log_step = 20

train_data = 'dataset/' + dataset + '.txt'
test_data = 'dataset/testdata/' + dataset + '_test.txt'
cat_train_data = 'dataset/' + dataset + '_cat{}.txt'
cat_test_data = 'dataset/testdata/' + dataset + '_cat{}_test.txt'

# ===Metrics===
use_nll_oracle = True
use_nll_gen = True
use_nll_div = True
use_bleu = True
use_self_bleu = True
use_clas_acc = True
use_ppl = False

# ===Generator===
ADV_g_step = 1  # 1
rollout_num = 16  # 4
gen_embed_dim = 32  # 32
gen_hidden_dim = 32  # 32
goal_size = 16  # LeakGAN-16
step_size = 4  # LeakGAN-4

mem_slots = 1  # RelGAN-1
num_heads = 2  # RelGAN-2
head_size = 256  # RelGAN-256

# ===Discriminator===
d_step = 5  # SeqGAN-50, LeakGAN-5
d_epoch = 3  # SeqGAN,LeakGAN-3
ADV_d_step = 5  # SeqGAN,LeakGAN,RelGAN-5
ADV_d_epoch = 3  # SeqGAN,LeakGAN-3

dis_embed_dim = 64
dis_hidden_dim = 64
num_rep = 64  # RelGAN

# ===log===
log_time_str = strftime("%m%d_%H%M_%S", localtime())
log_filename = strftime("log/log_%s" % log_time_str)
if os.path.exists(log_filename + '.txt'):
    i = 2
    while True:
        if not os.path.exists(log_filename + '_%d' % i + '.txt'):
            log_filename = log_filename + '_%d' % i
            break
        i += 1
log_filename = log_filename + '.txt'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# device=1
# print('device: ', device)
torch.cuda.set_device(device)

# ===Save Model and samples===
save_root = 'save/{}/{}/{}_{}_lt-{}_sl{}_temp{}_T{}/'.format(time.strftime("%Y%m%d"),
                                                             dataset, run_model, model_type,
                                                             loss_type, max_seq_len,
                                                             temperature,
                                                             log_time_str)
save_samples_root = save_root + 'samples/'
save_model_root = save_root + 'models/'

oracle_state_dict_path = 'pretrain/oracle_data/oracle_lstm.pt'
oracle_samples_path = 'pretrain/oracle_data/oracle_lstm_samples_{}.pt'
multi_oracle_state_dict_path = 'pretrain/oracle_data/oracle{}_lstm.pt'
multi_oracle_samples_path = 'pretrain/oracle_data/oracle{}_lstm_samples_{}.pt'

pretrain_root = 'pretrain/{}/'.format(dataset if if_real_data else 'oracle_data')
pretrained_gen_path = pretrain_root + 'gen_MLE_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type, max_seq_len,
                                                                                   samples_num)
pretrained_dis_path = pretrain_root + 'dis_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type, max_seq_len,
                                                                               samples_num)
pretrained_clas_path = pretrain_root + 'clas_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type, max_seq_len,
                                                                                 samples_num)
signal_file = 'run_signal.txt'

tips = ''


# Init settings according to parser
def init_param(opt):
    global run_model, model_type, loss_type, CUDA, device, data_shuffle, samples_num, vocab_size, \
        MLE_train_epoch, ADV_train_epoch, inter_epoch, batch_size, max_seq_len, start_letter, padding_idx, \
        gen_lr, gen_adv_lr, dis_lr, clip_norm, pre_log_step, adv_log_step, train_data, test_data, temp_adpt, \
        temperature, oracle_pretrain, gen_pretrain, dis_pretrain, ADV_g_step, rollout_num, gen_embed_dim, \
        gen_hidden_dim, goal_size, step_size, mem_slots, num_heads, head_size, d_step, d_epoch, \
        ADV_d_step, ADV_d_epoch, dis_embed_dim, dis_hidden_dim, num_rep, log_filename, save_root, \
        signal_file, tips, save_samples_root, save_model_root, if_real_data, pretrained_gen_path, \
        pretrained_dis_path, pretrain_root, if_test, dataset, PRE_clas_epoch, oracle_samples_path, \
        pretrained_clas_path, gen_init, dis_init, multi_oracle_samples_path, k_label, cat_train_data, cat_test_data, \
        use_nll_oracle, use_nll_gen, use_nll_div, use_bleu, use_self_bleu, use_clas_acc, use_ppl

    if_test = True if opt.if_test == 1 else False
    run_model = opt.run_model
    k_label = opt.k_label
    dataset = opt.dataset
    model_type = opt.model_type
    loss_type = opt.loss_type
    if_real_data = True if opt.if_real_data == 1 else False
    CUDA = True if opt.cuda == 1 else False
    device = opt.device
    data_shuffle = opt.shuffle
    gen_init = opt.gen_init
    dis_init = opt.dis_init

    samples_num = opt.samples_num
    vocab_size = opt.vocab_size
    MLE_train_epoch = opt.mle_epoch
    PRE_clas_epoch = opt.clas_pre_epoch
    ADV_train_epoch = opt.adv_epoch
    inter_epoch = opt.inter_epoch
    batch_size = opt.batch_size
    max_seq_len = opt.max_seq_len
    start_letter = opt.start_letter
    padding_idx = opt.padding_idx
    gen_lr = opt.gen_lr
    gen_adv_lr = opt.gen_adv_lr
    dis_lr = opt.dis_lr
    clip_norm = opt.clip_norm
    pre_log_step = opt.pre_log_step
    adv_log_step = opt.adv_log_step
    temp_adpt = opt.temp_adpt
    temperature = opt.temperature
    oracle_pretrain = True if opt.ora_pretrain == 1 else False
    gen_pretrain = True if opt.gen_pretrain == 1 else False
    dis_pretrain = True if opt.dis_pretrain == 1 else False

    ADV_g_step = opt.adv_g_step
    rollout_num = opt.rollout_num
    gen_embed_dim = opt.gen_embed_dim
    gen_hidden_dim = opt.gen_hidden_dim
    goal_size = opt.goal_size
    step_size = opt.step_size
    mem_slots = opt.mem_slots
    num_heads = opt.num_heads
    head_size = opt.head_size

    d_step = opt.d_step
    d_epoch = opt.d_epoch
    ADV_d_step = opt.adv_d_step
    ADV_d_epoch = opt.adv_d_epoch
    dis_embed_dim = opt.dis_embed_dim
    dis_hidden_dim = opt.dis_hidden_dim
    num_rep = opt.num_rep

    use_nll_oracle = True if opt.use_nll_oracle == 1 else False
    use_nll_gen = True if opt.use_nll_gen == 1 else False
    use_nll_div = True if opt.use_nll_div == 1 else False
    use_bleu = True if opt.use_bleu == 1 else False
    use_self_bleu = True if opt.use_self_bleu == 1 else False
    use_clas_acc = True if opt.use_clas_acc == 1 else False
    use_ppl = True if opt.use_ppl == 1 else False

    log_filename = opt.log_file
    signal_file = opt.signal_file
    tips = opt.tips

    # CUDA device
    torch.cuda.set_device(device)

    # Save path
    save_root = 'save/{}/{}/{}_{}_lt-{}_sl{}_temp{}_T{}/'.format(time.strftime("%Y%m%d"),
                                                                 dataset, run_model, model_type,
                                                                 loss_type, max_seq_len,
                                                                 temperature,
                                                                 log_time_str)
    save_samples_root = save_root + 'samples/'
    save_model_root = save_root + 'models/'

    train_data = 'dataset/' + dataset + '.txt'
    test_data = 'dataset/testdata/' + dataset + '_test.txt'
    cat_train_data = 'dataset/' + dataset + '_cat{}.txt'
    cat_test_data = 'dataset/testdata/' + dataset + '_cat{}_test.txt'

    if max_seq_len == 40:
        oracle_samples_path = 'pretrain/oracle_data/oracle_lstm_samples_{}_sl40.pt'
        multi_oracle_samples_path = 'pretrain/oracle_data/oracle{}_lstm_samples_{}_sl40.pt'

    pretrain_root = 'pretrain/{}/'.format(dataset if if_real_data else 'oracle_data')
    pretrained_gen_path = pretrain_root + 'gen_MLE_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type,
                                                                                       max_seq_len, samples_num)
    pretrained_dis_path = pretrain_root + 'dis_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type, max_seq_len,
                                                                                   samples_num)
    pretrained_clas_path = pretrain_root + 'clas_pretrain_{}_{}_sl{}_sn{}.pt'.format(run_model, model_type, max_seq_len,
                                                                                     samples_num)

    # Assertion
    assert k_label >= 2, 'Error: k_label = {}, which should be >=2!'.format(k_label)

    # Create Directory
    dir_list = ['save', 'savefig', 'log', 'pretrain', 'dataset',
                'pretrain/{}'.format(dataset if if_real_data else 'oracle_data')]
    if not if_test:
        dir_list.extend([save_root, save_samples_root, save_model_root])
    for d in dir_list:
        if not os.path.exists(d):
            os.makedirs(d)
