<template>
	<view class="background">
		<!-- <h1>普通团员功能待开发中</h1> -->
		<view class="glass">
			<view class="main">
				<h1>青年大学习提醒软件</h1>
				<br>
				<h2>请您填写您的QQ号码</h2>
				<h2>以便我们可以提醒您</h2>
				<h2>及时完成青年大学习</h2>
				<br><br>
				<view login-form>
					<view>
						<input @input="QQnumberInput" type="text" v-model="QQnumber" class="inputQQ" placeholder="请输入您的QQ号码" />
					</view>
					<view>
						<button @click="formSubmit()" class="login-btn">
							确定
						</button>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import baseUrl from '../../config.js'
	export default {
		data() {
			return {
				QQnumber: '',
				item: '',
				list: '',
				type: '',
			}
		},
		onLoad: function(option) { //option为object类型，会序列化上个页面传递的参数
			console.log(option)
			const Genitem = JSON.parse(decodeURIComponent(option.Genitem))
			const list = JSON.parse(decodeURIComponent(option.list))
			const type = option.type
			this.Genitem = Genitem
			this.list = list
			this.type = type
		},
		methods: {
			QQnumberInput(e) {
				this.QQnumber = e.target.value
			},
			formSubmit: function() {
				var that = this;
				// console.log(that.list["UserName"])
				if (that.QQnumber == '') {
					uni.showToast({
						title: '请输入您的QQ账号',
						icon: 'none',
						duration: 2000
					});
				} else if (that.QQnumber.length < 5) {
					uni.showToast({
						title: '请认真填写',
						icon: 'none',
						duration: 2000
					});
				} else {
					uni.showModal({
						title: that.QQnumber,
						content: '请您再次确定您的QQ号码',
						success: function(res) {
							if (res.confirm) {
								uni.request({
									url: "http://127.0.0.1:5000/init_email",
									method: 'POST',
									header: {
										'content-type': 'application/x-www-form-urlencoded',
									},
									data: {
										QQEmail: that.QQnumber + "@qq.com",
										UserName: that.list["UserName"],
										acctId: that.list["acctId"],
										colName: that.list["colName"],
										grade: that.list["grade"],
										major: that.list["major"],
										positionName: that.list["positionName"],
										schoolName: that.list["schoolName"],
									},
									success(res) {
										if (res.data.msg === 200) {
											uni.showToast({
												title: '争做新青年',
												icon: 'success',
												duration: 2000
											});
											if (that.type === 2) {
												const listNum = that.list
												uni.navigateTo({
													url: `../index/index?list=${encodeURIComponent(JSON.stringify(listNum))}`,
													animationType: 'fade-in',
													animationDuration: 2000
												});
											} else {
												uni.navigateTo({
													url: `../normal/normal`,
													animationType: 'fade-in',
													animationDuration: 2000
												});
											}
										} else {
											uni.navigateTo({
												url: `../normal/normal`,
												animationType: 'fade-in',
												animationDuration: 2000
											});
										}
									}
								})
							} else if (res.cancel) {
								console.log('用户点击取消');
							}
						}
					});
				}
			}
		}
	}
</script>

<style>
	* {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
		font-family: Helvetica, sans-serif;
	}

	.background {
		width: 100vw;
		height: 90vh;
		max-width: 100%;
		/* background: url("./1.jpg") no-repeat; */
		/* background: rgb(203, 210, 240); */
		background: #FFFFFF;
		background-size: cover;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.glass {
		width: 80vw;
		height: 80vh;
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		background-color: rgb(203, 210, 240);
		/* background-color: #ffffff; */
		box-shadow: 0 8px 32px 0 rgba(27, 0, 37, 0.89);
		border-radius: 10px;
	}

	.background>h1 {
		position: absolute;
		font-size: 10vw;
		/* color: #c8a3ff; */
		color: #d8a5e2;
	}

	.glass .main {
		margin-top: 40%;
	}

	.glass .main h1 {
		text-align: center;
		padding-top: 0.2em;
		font-size: 8vw;
		color: #ffffff;
		text-shadow: 1px 1px 12px rgba(255, 255, 255, 0.2);
		font-size: 60rpx;
		text-shadow: 2px 2px 6px #B382F9
	}

	.glass .main h2 {
		text-align: center;
		color: #ffffff;
		font-size: 40rpx;
		text-shadow: 2px 2px 6px #C0A5F3
	}

	.glass .main .inputQQ {
		padding: 16px 52px 16px 18px;
		border-radius: 48px;
		border: none;
		outline: none;
		box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.08);
		width: 80%;
		height: 40%;
		font-size: 16px;
		color: #626262;
		margin: 30px 30px 30px 30px;
	}

	.glass .main .login-btn {
		margin: 6px 0;
		height: 40%;
		border: none;
		background-color: rgba(255, 255, 255, 0.3);
		border-radius: 10px;
		padding: 0 14px;
		color: #3d5245;
		margin: 30px 30px 30px 30px;
	}
</style>
