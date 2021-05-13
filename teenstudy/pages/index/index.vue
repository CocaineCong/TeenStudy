<template>
	<main>
		<view class="container">
			<view class="big_title">
				<h1>学习新思想</h1>
				<h1>争做新青年</h1>
			</view>

			<view class="input-add">
				<input type="text" name="todo" v-model="message" />
				<button class="send_mail" @click="send_mail">一键提醒
					<!-- <i class="plus"></i> -->
				</button>
			</view>

			<view class="filters">
				<span class="filter active">未完成</span>
				<!-- 				<span class="filter">已完成</span>
				<span class="filter">未完成</span> -->
			</view>

			<view class="todo-list">
				<view class="todo-item" v-if="list.length!==0" v-for="(list,index) in list" :key="index">
					<label>
						<span style="margin-left: 200rpx;">{{list.name}}</span>
						<span class="check-button"></span>
					</label>
				</view>
				<view class="todo-item" v-if="list.length===0">
					<label>
						<span style="margin-left: 150rpx;">全都完成啦~~</span>
						<span class="check-button"></span>
					</label>
				</view>
			</view>

		</view>
	</main>

</template>

<script>
	export default {
		name: "index",
		data() {
			return {
				message: '一键提醒',
				list: []
			}
		},
		onLoad: function(option) { //option为object类型，会序列化上个页面传递的参数
			console.log("option")
			console.log(option)
			// console.log("option-item")
			// console.log(option.list)
			var item = JSON.parse(decodeURIComponent(option.list))
			if (item == "0") {
				this.list = []
			} else {
				this.list = item
			}
			// console.log("LIST")
			// console.log(this.list)
		},
		methods: {
			send_mail: function() {
				// var that = this
				console.log(this.list)
				var item = []
				for (var i = 0; i < this.list.length; i++) {
					var temp = this.list[i]
					var email = []
					email.push(temp.email)
					email.push(temp.name)
					item.push(email)
				}
				uni.request({
					url: "http://127.0.0.1:5000/sendMail",
					method: 'POST',
					header: {
						'content-type': 'application/x-www-form-urlencoded',
					},
					data: {
						EmailList: item,
					},
					success(res) {
						console.log("TEST")
						console.log(res)
						if (res.data.code == "200")
							uni.showToast({
								title: '提醒成功',
								icon: 'success',
								duration: 2000
							});
					}
				})

			}
		}
	}
</script>

<style>
	* {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
		font-family: Helvetica, "PingFang SC", "Microsoft Yahei", sans-serif;
	}

	/* 整个页面 */
	main {
		width: 100vw;
		min-height: 100vh;
		/* min-height: auto; */
		height: auto;
		display: grid;
		align-items: center;
		justify-items: center;
		background: rgb(203, 210, 240);
	}

	.container {
		width: 85%;
		height: auto;
		/* 		height: 90%; */
		max-width: 400px;
		margin-top: 60rpx;
		margin-bottom: 60rpx;
		box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.15);
		border-radius: 24px;
		padding: 10px 28px;
		background-color: rgb(245, 246, 252);
	}

	.big_title {
		/* border: 1rpx solid #4CD964; */
		/* position: absolute; */

	}

	/* 标题 */
	.big_title h1 {
		margin: 10px 0;
		font-size: 28px;
		color: #414873;
		text-align: center;
	}

	/* 添加框 */
	.input-add {
		position: relative;
		display: flex;
		align-items: center;
		padding: 20px;
	}

	.input-add input {
		padding: 16px 52px 16px 18px;
		border-radius: 48px;
		border: none;
		outline: none;
		box-shadow: 0px 0px 24px rgba(0, 0, 0, 0.08);
		width: 100%;
		font-size: 16px;
		color: #626262;
	}

	.input-add button {
		width: 100px;
		height: 46px;
		border-radius: 6%;
		background: linear-gradient(#c0a5f3, #7f95f7);
		border: none;
		outline: none;
		color: white;
		position: absolute;
		right: 0px;
		cursor: pointer;
	}

	.input-add .plus {
		display: block;
		width: 100%;
		height: 100%;
		background: linear-gradient(#fff, #fff), linear-gradient(#fff, #fff);
		background-size: 50% 2px, 2px 50%;
		background-position: center;
		background-repeat: no-repeat;
	}

	.filters {
		display: flex;
		margin: 20rpx 2rpx;
		color: #c0c2ce;
		font-size: 14px;
	}

	.filters .filter {
		margin-right: 14px;
		transition: 0.8s;
	}

	.filters .filter.active {
		color: #6b729c;
		transform: scale(1.2);
	}

	.todo-list {
		display: grid;
		height: 68%;
		row-gap: 10px;
		/* overflow: hidden; */
		/* overflow-y: scroll; */
	}

	.todo-item {
		background: white;
		padding: 16px;
		border-radius: 8px;
		color: #626262;
	}

	.todo-item label {
		position: relative;
		display: flex;
		align-items: center;
	}

	.todo-item label span.check-button {
		position: absolute;
		top: 0;
	}

	.todo-item label span.num {

		top: 0;
	}

	.todo-item label span.check-button::before,
	.todo-item label span.check-button::after {
		content: "";
		display: block;
		position: absolute;
		width: 18px;
		height: 18px;
		border-radius: 50%;
	}

	.todo-item label span.check-button::before {
		border: 1px solid #b382f9;
	}

	.todo-item label span.check-button::after {
		transition: 0.4s;
		background: #b382f9;
		transform: translate(1px, 1px) scale(0.8);
		opacity: 0;
	}

	.todo-item input {
		margin-right: 16px;
		opacity: 0;
	}

	.todo-item input:checked+span.check-button::after {
		opacity: 1;
	}
</style>
