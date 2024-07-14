<template>
  <div class="view-logs">
    <h2>告警日志</h2>
    <el-table :data="logData" style="width: 100%">
      <el-table-column prop="timestamp" label="时间" width="180"></el-table-column>
      <el-table-column prop="message" label="告警信息"></el-table-column>
    </el-table>
    <el-pagination
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="pageSize"
        layout="total, prev, pager, next"
        :total="total">
    </el-pagination>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewLogs',
  data() {
    return {
      logData: [],
      currentPage: 1,
      pageSize: 10,
      total: 0
    };
  },
  created() {
    this.fetchLogs();
  },
  methods: {
    async fetchLogs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/logs', {
          params: {
            page: this.currentPage,
            pageSize: this.pageSize
          }
        });
        this.logData = response.data.logs;
        this.total = response.data.total;
      } catch (error) {
        console.error('Error fetching logs:', error);
        this.$message.error('获取日志失败，请稍后再试');
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchLogs();
    }
  }
}
</script>

<style scoped>
.view-logs {
  padding: 20px;
}
</style>