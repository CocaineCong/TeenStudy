<template>
	<view class="content">
		<view class="login" @submit="formSubmit">

			<view class="content-wrapper">
				<view class="title">
					<h1><strong>登陆</strong></h1>
				</view>

				<view class="login-form">
					<view class="login-form-items">
						<view class="login-form-items-title">手机号</view>
						<input @input="OnUserInput" type="text" v-model="username" class="login-input" placeholder="手机号" />
					</view>
				</view>

				<view class="login-form">
					<view class="login-form-items">
						<view class="login-form-items-title">密码</view>
						<input @input="OnPwdInput" type="password" v-model="password" class="login-input" placeholder="请输入登录密码" />
					</view>
				</view>

				<view class="submit-wrapper test">
					<button type="primary" :loading='loading' @click="formSubmit()" @tap="formSubmit()" class="login-btn">登陆</button>
				</view>
			</view>

		</view>
	</view>
</template>

<script>
	import util from '../../utils/util.js'
	import baseUrl from '../../config.js'
	export default {
		data() {
			return {
				loading: false,
				username: '',
				password: '',
				NumList: [],
			}
		},
		methods: {
			OnUserInput(e) {
				this.username = e.target.value
			},
			OnPwdInput(e) {
				this.password = e.target.value
			},
			formSubmit: function() {
				var that = this;
				if (that.username === "" || that.password === "") {
					uni.showModal({
						title: '提示',
						content: '请正确输入账号密码',
						success: function(res) {
							if (res.confirm) {
								console.log('用户点击确定');
							} else if (res.cancel) {
								console.log('用户点击取消');
							}
						}
					});
					// uni.showToast({
					//     title: '请输入用户名或是密码',
					//     duration: 2000
					// });
					return
				}
				uni.request({
					url: "http://127.0.0.1:5000/login",
					method: 'POST',
					header: {
						'content-type': 'application/x-www-form-urlencoded',
					},
					data: {
						username: that.username,
						password: that.password,
					},
					success(res) {
						if (res.statusCode === 200) { //判断是不是请求成功
							if (res.data.msg === 3) { //判断是不是团支书
								if (res.data.info === 10001) {
									const Genitem = res.data.infoDetail
									uni.navigateTo({
										url: `../generate/generate?type=3&item=${encodeURIComponent(JSON.stringify(Genitem))}`,
										animationType: 'fade-in',
										animationDuration: 2000
									});
									return
								} else if (res.data.info === 10002) {
									uni.navigateTo({ //后期可以在这里加上修改Email
										url: `../normal/normal`,
										animationType: 'fade-in',
										animationDuration: 2000
									});
									return
								}
							} else if (res.data.msg === 2) {
								if (res.data.info === 10001) {
									const Genitem = res.data.infoDetail
									const list = res.data.data
									uni.navigateTo({
										url: `../generate/generate?type=2&Genitem=${encodeURIComponent(JSON.stringify(Genitem))}&list=${encodeURIComponent(JSON.stringify(list))}`,
										animationType: 'fade-in',
										animationDuration: 2000
									});
								} else if (res.data.info === 10002) {
									console.log("RES")
									console.log(res)
									that.NumList = res.data.data
									const list = that.NumList
									uni.navigateTo({
										url: `../index/index?type=1&list=${encodeURIComponent(JSON.stringify(list))}`,
										animationType: 'fade-in',
										animationDuration: 300
									});
								}
							} else {
								uni.showToast({
									title: '出现了一点错误,请稍后重试',
									icon: 'none',
									duration: 2000
								});
							}
						} else {
							uni.showToast({
								title: '出现了一点错误,请稍后重试',
								icon: 'none',
								duration: 2000
							});
						}
					}
				})
			}
		}
	}
</script>

<style lang="scss">
	page {
		background: #F8F8F8;
	}

	.content {
		height: auto;
		min-height: 100rpx;
	}

	.login {
		height: auto;

		.content-wrapper {
			position: absolute;
			width: 100%;
			margin: 40% auto;

			.title {
				width: 100%;

				h1 {
					border: 0px;
					width: 50%;
					margin: 0 auto;
					text-align: center;
					border-bottom: 1px solid #E3E3E3;
					height: 50px;
					font-weight: bolder;
					line-height: 50px;
					font-size: 27px;
					overflow: hidden;
					font-weight: 400;
				}
			}

			.login-form {
				margin: 30px 30px 30px 30px;
				background: #FFFFFF;

				.login-form-items {
					margin-top: 20rpx;
					padding: 15px 10px;
					border-bottom: 2px solid #F3F4F5;
					position: relative;
					display: -webkit-flex;
					display: flex;

					.login-form-items-title {
						width: 30%;
						line-height: 22px;
						height: 22px;
						flex-shrink: 0;
						text-align: center;
						font-weight: normal;
					}

					.login-input {
						width: 100%
					}
				}
			}
		}

		.submit-wrapper {
			padding: 29px;
			padding-top: 8px;
		}

	}
</style>
