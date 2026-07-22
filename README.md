# 🚀 Complete Step-by-Step Guide
## AI Background Remover — AWS Setup 

> **Hinglish me hai** — Sabse pehle poora padho, phir start karo.  


---

## 📌 Kya Kya Banayenge?

```
User (Browser)
    ↓  image upload
EC2 (Flask Website)
    ↓  S3 me save karo
S3 Bucket → input/ folder
    ↓  automatic trigger
Lambda Function
    ↓  EFS se rembg library load karo
EFS (AI Libraries + Model)
    ↓  background remove
S3 Bucket → output/ folder
    ↓  result dikhao
User ko Clean PNG
```

---

## ✅ Master Checklist (Tick karte jao)

- [ ] **PART 1** — S3 Bucket banana
- [ ] **PART 2** — IAM Roles banana
- [ ] **PART 3** — EFS banana
- [ ] **PART 4** — EC2 pe Files + App Setup
- [ ] **PART 5** — EC2 pe EFS Mount + Libraries Install
- [ ] **PART 6** — Lambda Function Setup
- [ ] **PART 7** — VPC S3 Endpoint (Critical!)
- [ ] **PART 8** — Final Test

---

## ⚠️ Shuru Karne Se Pehle — Region Check Karo

AWS Console ke **top-right corner** me region dekhna.  
Poori setup me **EK HI REGION** use karo.  
Recommended: `ap-south-1` (Asia Pacific Mumbai)

> 💡 **Ek region set karo aur mat badlo!**

---

---

# PART 1 — S3 BUCKET BANANA

**S3 kya hai?** Ek online storage box jisme original aur processed images store hongi.

---

### Step 1.1 — S3 Console Kholo

```
AWS Console → Search bar me "S3" type karo → S3 click karo
```

---

### Step 1.2 — Bucket Banao

1. **"Create bucket"** button click karo
2. Fill karo:
   | Field | Value |
   |-------|-------|
   | Bucket name | `bg-remover-images-123` *(koi bhi unique naam)* |
   | AWS Region | `ap-south-1` |
   | Block all public access | ✅ ON raho (default) |
3. Baaki sab **default** rehne do
4. **"Create bucket"** click karo

> ✅ **Check:** Bucket list me naam dikhne laga? Good!

> 📝 **Note:** Bucket naam kahin likh lo — baad me `app.py` aur Lambda me use hoga.

---

---

# PART 2 — IAM ROLES BANANA
### ⏱ Time: ~10 minutes

**IAM Role kya hai?** Permission card. EC2 aur Lambda ko S3 access karne ki permission deta hai.

---

### Step 2.1 — EC2 ke liye Role Banao

```
AWS Console → IAM → Roles (left menu) → "Create role"
```

1. **Trusted entity type:** `AWS service`
2. **Use case:** `EC2` select karo
3. **Next**
4. **Permissions** me search karo: `AmazonS3FullAccess`
   - Checkbox laga do ✅
5. **Next**
6. **Role name:** `ec2-bg-remover-role`
7. **"Create role"** click karo

> ✅ **Check:** Role list me `ec2-bg-remover-role` dikh raha hai?

---

### Step 2.2 — Lambda ke liye Role Banao

```
IAM → Roles → "Create role"
```

1. **Trusted entity type:** `AWS service`
2. **Use case:** `Lambda` select karo
3. **Next**
4. **Permissions** me teen policies add karo:
   - `AmazonS3FullAccess` ✅
   - `AWSLambdaVPCAccessExecutionRole` ✅
   - `AmazonElasticFileSystemClientReadWriteAccess` ✅
5. **Next**
6. **Role name:** `lambda-bg-remover-role`
7. **"Create role"** click karo

> ✅ **Check:** Dono roles list me dikh rahe hain?

---

---

# PART 3 — EFS (ELASTIC FILE SYSTEM) BANANA

**EFS kya hai?** Ek shared network drive. EC2 pe libraries install karo → Lambda automatically wahi se read karega.

---

### Step 3.1 — EFS Console Kholo

```
AWS Console → Search bar me "EFS" → EFS click karo
```

---

### Step 3.2 — File System Banao

1. **"Create file system"** click karo
2. Fill karo:
   | Field | Value |
   |-------|-------|
   | Name | `bg-remover-efs` |
   | VPC | **Default VPC** select karo |
3. **"Create"** click karo

> ⏳ 1-2 minutes wait karo jab tak "Available" show kare.

---

### Step 3.3 — File System ID Copy Karo

1. Apna EFS click karo
2. **File system ID** copy karo — kuch aisa dikhega: `fs-0abc1234567890def`
3. Notepad me save karo 📝

---

### Step 3.4 — Access Point Banao

1. EFS → apna filesystem → **"Access points"** tab
2. **"Create access point"** click karo
3. Fill karo:
   | Field | Value |
   |-------|-------|
   | Name | `bg-remover-ap` |
   | Root directory path | `/` |
4. **POSIX user** section:
   | Field | Value |
   |-------|-------|
   | User ID | `1000` |
   | Group ID | `1000` |
5. **Root directory creation permissions** section:
   | Field | Value |
   |-------|-------|
   | Owner user ID | `1000` |
   | Owner group ID | `1000` |
   | POSIX permissions | `777` |
6. **"Create access point"** click karo

> ✅ Access Point ID bhi copy karo — `fsap-XXXXXXXXX` — notepad me save karo 📝

---

### Step 3.5 — EFS Security Group Check Karo

```
EFS → apna filesystem → "Network" tab
```

Har Availability Zone ke liye ek Security Group dikh raha hoga.  
**Kuch karna nahi** — default SG automatically allow karta hai. Bas check karo ki "Available" show ho raha ho.

---

---

# PART 4 — EC2 PE FILES + APP SETUP

**EC2 kya karta hai?** Yahan Flask website chalegi. Users yahan image upload karenge.

---

### Step 4.1 — EC2 ka IAM Role Attach Karo

```
EC2 Console → Instances → Apna instance select karo
→ Actions → Security → Modify IAM role
→ IAM role: "ec2-bg-remover-role" select karo
→ Update IAM role
```

---

### Step 4.2 — EC2 Security Group me Port 5000 Open Karo

```
EC2 → Instances → Apna instance → Security tab
→ Security groups link click karo
→ "Edit inbound rules" click karo
→ "Add rule" click karo
```

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| Custom TCP | TCP | 5000 | 0.0.0.0/0 |

**"Save rules"** click karo.

---

### Step 4.3 — EC2 SSH Connection Karo

EC2 Console → Apna instance → **"Connect"** button → EC2 Instance Connect → Connect

*Ya apne terminal se:*
```bash
ssh -i "apni-key.pem" ubuntu@EC2-PUBLIC-IP
```

---

### Step 4.4 — Project Folder Banao

EC2 terminal me yeh commands ek ek karke chalao:

```bash
# Folder structure banao
mkdir -p ~/bg-remover/templates

# Dependencies install karo
sudo apt update && sudo apt upgrade -y
pip3 install flask boto3 gunicorn werkzeug --break-system-packages
```

---

### Step 4.5 — app.py File Banao

```bash
nano ~/bg-remover/app.py
```

Github pr jo app.py ka code paste kr do, (**APNA BUCKET NAAM DAALO**):

> **Nano me save karne ke liye:** `Ctrl+X` → `Y` → `Enter`

---

### Step 4.6 — index.html File Banao

```bash
nano ~/bg-remover/templates/index.html
```

Pehle github share kiya gaya `index.html` ka poora code yahan paste karo.

> **Nano me save:** `Ctrl+X` → `Y` → `Enter`

---

---

# PART 5 — EC2 PE EFS MOUNT + LIBRARIES INSTALL

---

### Step 5.1 — EFS Mount Karo (EC2 terminal me)

```bash
# EFS utils install karo
sudo apt-get install -y amazon-efs-utils

# Mount folder banao
sudo mkdir -p /mnt/efs
sudo chmod 777 /mnt/efs

# EFS mount karo — APNA EFS ID DAALO
sudo mount -t efs -o tls fs-XXXXXXXXXX:/ /mnt/efs
```

> 📝 `fs-XXXXXXXXXX` ki jagah apna EFS ID daalo (Part 3.3 me save kiya tha)

**Mount verify karo:**
```bash
df -h /mnt/efs
# Output me /mnt/efs dikhna chahiye
```

> ✅ **Agar mount ho gaya** to next step pe jao.  
> ❌ **Agar error aaya** to EC2 aur EFS ka VPC same hai ya nahi check karo.

---

### Step 5.2 — Reboot ke baad bhi Mount Rahe

```bash
echo "fs-XXXXXXXXXX:/ /mnt/efs efs defaults,_netdev 0 0" | sudo tee -a /etc/fstab
```

> 📝 Apna EFS ID daalna mat bhoolna!

---

### Step 5.3 — EFS pe Folders Banao

```bash
mkdir -p /mnt/efs/lib/python3.14/site-packages
mkdir -p /mnt/efs/models
```

---

### Step 5.4 — EFS pe Libraries Install Karo


```bash
pip3 install rembg onnxruntime Pillow numpy scipy pymatting pooch \
    --target /mnt/efs/lib/python3.14/site-packages \
    --no-cache-dir \
    --break-system-packages
```

**Size check karo:**
```bash
du -sh /mnt/efs/lib/
# ~1.5GB hona chahiye
```

---

### Step 5.5 — AI Model EFS pe Download Karo

> ⏳ ~170MB download hoga — internet speed pe depend karta hai

```bash
python3 - <<'EOF'
import sys, os
sys.path.insert(0, '/mnt/efs/lib/python3.14/site-packages')
os.environ['U2NET_HOME'] = '/mnt/efs/models'
print("Model download ho raha hai...")
from rembg import new_session
new_session('u2net')
print("✅ Model download complete!")
EOF
```

**Verify karo:**
```bash
ls -lh /mnt/efs/models/
# u2net.onnx dikhna chahiye (~168MB)
```

---

### Step 5.6 — Flask App Start Karo

```bash
cd ~/bg-remover
export S3_BUCKET="bg-remover-images-123"   # APNA BUCKET NAAM
export AWS_REGION="ap-south-1"
python3 app.py
```

**Test karo:** Browser me `http://EC2-PUBLIC-IP:5000` kholo — website dikhni chahiye! 🎉

> 💡 App background me chalate rehne ke liye:
> ```bash
> nohup python3 app.py &
> ```

---

---

# PART 6 — LAMBDA FUNCTION SETUP

---

### Step 6.1 — Lambda Function Banao (ya existing update karo)

```
AWS Console → Lambda → Functions
```

**Naya function hai to:**
1. **"Create function"** click karo
2. **Author from scratch** select karo
3. Fill karo:
   | Field | Value |
   |-------|-------|
   | Function name | `bg-remover-lambda` |
   | Runtime | `Python 3.14` |
   | Architecture | `x86_64` |
4. **Permissions** → `Use an existing role` → `lambda-bg-remover-role`
5. **"Create function"** click karo

---

### Step 6.2 — Lambda Code Upload Karo

Lambda Console → apna function → **Code** tab:


*Isme github pr diya gya lambda_function.py  directly code editor me paste karo:*

```

**"Deploy"** button click karo.

---

### Step 6.3 — Lambda VPC Set Karo

```
Lambda → apna function → Configuration → VPC → Edit
```

| Field | Value |
|-------|-------|
| VPC | Default VPC (wahi jo EFS me select kiya tha) |
| Subnets | Saare subnets select karo |
| Security groups | Default security group |

**"Save"** click karo.

---

### Step 6.4 — Lambda EFS Attach Karo

```
Lambda → Configuration → File systems → Add
```

| Field | Value |
|-------|-------|
| EFS file system | `bg-remover-efs` |
| EFS access point | `bg-remover-ap` |
| Local mount path | `/mnt/efs` |

**"Save"** click karo.

---

### Step 6.5 — Environment Variables Set Karo

```
Lambda → Configuration → Environment variables → Edit → Add
```

| Key | Value |
|-----|-------|
| `PYTHONPATH` | `/mnt/efs/lib/python3.14/site-packages` |
| `U2NET_HOME` | `/mnt/efs/models` |

**"Save"** click karo.

---

### Step 6.6 — Timeout aur Memory Set Karo

```
Lambda → Configuration → General configuration → Edit
```

| Field | Value |
|-------|-------|
| Memory | `2048` MB |
| Timeout | `5` min `0` sec |

**"Save"** click karo.

---

### Step 6.7 — S3 Trigger Add Karo

```
Lambda → Configuration → Triggers → Add trigger
```

| Field | Value |
|-------|-------|
| Source | `S3` |
| Bucket | `bg-remover-images-123` (apna bucket) |
| Event types | `PUT` |
| Prefix | `input/` |

> ⚠️ S3 same-bucket recursion warning aayegi — **"I acknowledge..."** checkbox tick karo

**"Add"** click karo.

---

---

# PART 7 — VPC S3 ENDPOINT (CRITICAL STEP!)

> ⚠️ **Yeh step skip mat karna!**  
> Lambda VPC me hone ke baad bina S3 Endpoint ke S3 se connect NAHI kar sakta.  
> Agar yeh nahi banaya to image process hogi lekin output S3 me save NAHI hoga — silently fail!

---

### Step 7.1 — VPC Endpoint Banao

```
AWS Console → VPC → Endpoints (left menu) → "Create endpoint"
```

Fill karo:

| Field | Value |
|-------|-------|
| Name | `s3-gateway-endpoint` |
| Service category | `AWS services` |
| Services search | `s3` type karo → `com.amazonaws.ap-south-1.s3` select karo (Gateway type) |
| VPC | Default VPC |
| Route tables | Jo bhi route tables dikhein — **saare select karo** |

**"Create endpoint"** click karo.

> ✅ Status "Available" dikhega thodi der me.

---

---

# PART 8 — FINAL TEST

---

### Step 8.1 — Website Test Karo

Browser me kholo:
```
http://EC2-PUBLIC-IP:5000
```

Website dikhni chahiye! ✨

---

### Step 8.2 — Image Upload Karo

1. Koi bhi image (JPG/PNG) website pe upload karo
2. Processing animation dikhega
3. 30-60 seconds baad result aana chahiye

---

### Step 8.3 — Agar Result Nahi Aaya — CloudWatch Check Karo

```
AWS Console → CloudWatch → Log groups
→ /aws/lambda/bg-remover-lambda
→ Latest log stream click karo
```

Error dekho aur iske steps se match karo:

| Error | Fix |
|-------|-----|
| `No module named 'rembg'` | EFS libraries sahi se install nahi huin — Part 5.4 dobara karo |
| `Unable to mount EFS` | Lambda VPC aur EFS ka VPC same nahi hai — Part 6.3 check karo |
| `Connection timeout` (S3) | VPC S3 Endpoint nahi banaya — Part 7 karo |
| `AccessDenied` | Lambda IAM Role me permissions nahi — Part 2.2 check karo |

---

---

## 📋 Quick Reference — Important Values

| Cheez | Apna Value |
|-------|------------|
| S3 Bucket Name | _________________ |
| EFS ID | fs-_________________ |
| EFS Access Point ID | fsap-_________________ |
| EC2 Public IP | _________________ |
| AWS Region | ap-south-1 |
| Lambda Function Name | bg-remover-lambda |

*(Yeh table fill karte jao setup ke dauran)*

---

## 🏁 Setup Complete!

Sab kuch sahi se kiya to:
- ✅ `http://EC2-IP:5000` pe website chalegi
- ✅ Image upload hogi → S3 `input/` folder me jayegi
- ✅ Lambda trigger hoga → `rembg` se background remove hoga
- ✅ Output `output/` folder me save hoga
- ✅ Website pe result + download button dikhega

---

*Koi bhi step me problem aaye to CloudWatch logs dekho aur exact error message chatgpt se help lo!*
